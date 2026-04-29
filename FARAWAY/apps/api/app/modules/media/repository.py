from __future__ import annotations

from sqlalchemy.orm import Session

from app.modules.media.model import MediaAsset


def create_media_asset(
    session: Session,
    *,
    user_id: str,
    media_type: str,
    storage_provider: str,
    storage_key: str,
    public_url: str,
) -> MediaAsset:
    asset = MediaAsset(
        user_id=user_id,
        media_type=media_type,
        storage_provider=storage_provider,
        storage_key=storage_key,
        public_url=public_url,
    )
    session.add(asset)
    session.flush()
    return asset
