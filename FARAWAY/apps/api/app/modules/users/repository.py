from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.media.model import MediaAsset
from app.modules.users.model import User


def get_user_by_id(session: Session, user_id: str) -> User | None:
    return session.get(User, user_id)


def user_owns_media_url(session: Session, user_id: str, public_url: str) -> bool:
    asset = session.execute(
        select(MediaAsset).where(MediaAsset.user_id == user_id, MediaAsset.public_url == public_url)
    ).scalar_one_or_none()
    return asset is not None
