from __future__ import annotations

from dataclasses import dataclass
import logging
from pathlib import Path
from uuid import uuid4

import oss2
from fastapi import HTTPException, UploadFile, status

from app.core.config import settings

logger = logging.getLogger(__name__)


@dataclass
class UploadResult:
    url: str
    filename: str


def _missing_oss_fields() -> list[str]:
    missing = []
    if not settings.oss_access_key_id or "你的AccessKey ID" in settings.oss_access_key_id:
        missing.append("OSS_ACCESS_KEY_ID")
    if not settings.oss_access_key_secret or "你的AccessKey Secret" in settings.oss_access_key_secret:
        missing.append("OSS_ACCESS_KEY_SECRET")
    if not settings.oss_endpoint:
        missing.append("OSS_ENDPOINT")
    if not settings.oss_bucket_name or "你的Bucket名称" in settings.oss_bucket_name:
        missing.append("OSS_BUCKET_NAME")
    return missing


async def upload_media(file: UploadFile, media_type: str, user_id: str, request_base_url: str | None = None) -> UploadResult:
    del request_base_url
    content = await file.read()
    max_mb = settings.max_image_size_mb if media_type == "image" else settings.max_video_size_mb
    if len(content) > max_mb * 1024 * 1024:
        raise HTTPException(status_code=413, detail=f"{media_type} file too large")

    ext = Path(file.filename or "").suffix or (".jpg" if media_type == "image" else ".mp4")
    filename = f"{uuid4().hex}{ext}"
    missing = _missing_oss_fields()
    if missing:
        logger.error("OSS upload blocked: missing configuration fields: %s", ", ".join(missing))
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Aliyun OSS is not configured. Missing: {', '.join(missing)}",
        )

    key = f"{settings.oss_upload_prefix.strip('/')}/{media_type}/{user_id}/{filename}"
    logger.info(
        "Starting OSS upload: media_type=%s user_id=%s key=%s bucket=%s endpoint=%s",
        media_type,
        user_id,
        key,
        settings.oss_bucket_name,
        settings.oss_endpoint,
    )

    auth = oss2.Auth(settings.oss_access_key_id, settings.oss_access_key_secret)
    bucket = oss2.Bucket(auth, settings.oss_endpoint, settings.oss_bucket_name)
    try:
        bucket.put_object(key, content)
    except Exception as exc:
        logger.exception(
            "OSS upload failed: media_type=%s user_id=%s key=%s bucket=%s endpoint=%s",
            media_type,
            user_id,
            key,
            settings.oss_bucket_name,
            settings.oss_endpoint,
        )
        raise HTTPException(status_code=502, detail=f"Aliyun OSS upload failed: {exc}") from exc

    if settings.oss_public_base_url:
        base = settings.oss_public_base_url.rstrip("/")
        url = f"{base}/{key}"
    else:
        endpoint_host = settings.oss_endpoint.removeprefix("https://").removeprefix("http://")
        url = f"https://{settings.oss_bucket_name}.{endpoint_host}/{key}"
    logger.info("OSS upload succeeded: key=%s url=%s", key, url)
    return UploadResult(url=url, filename=filename)
