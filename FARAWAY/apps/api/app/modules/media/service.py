from __future__ import annotations

import logging
from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.constants import ALLOWED_IMAGE_TYPES
from app.core.transactions import managed_transaction
from app.modules.media.repository import create_media_asset

logger = logging.getLogger(__name__)


async def upload_image(session: Session, user_id: str, file: UploadFile) -> dict:
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="unsupported image type")

    content = await file.read()
    max_size = settings.max_image_size_mb * 1024 * 1024
    if len(content) > max_size:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="image too large")

    extension = ALLOWED_IMAGE_TYPES[file.content_type]
    storage_key = f"avatars/{user_id}/{uuid4().hex}{extension}"
    target_path = settings.resolved_local_media_dir / storage_key
    target_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        target_path.write_bytes(content)
    except OSError as exc:
        logger.exception("local image upload failed user_id=%s path=%s", user_id, target_path)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="image upload failed") from exc

    public_url = f"{settings.media_url_prefix}/{storage_key}"
    with managed_transaction(session):
        asset = create_media_asset(
            session,
            user_id=user_id,
            media_type="image",
            storage_provider="local",
            storage_key=storage_key,
            public_url=public_url,
        )

    return {"asset_id": asset.id, "url": public_url}
