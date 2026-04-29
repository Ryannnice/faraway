from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.modules.content.model import ContentItem, ContentMedia
from app.modules.media.model import MediaAsset
from app.modules.users.model import User


def create_content(
    session: Session,
    *,
    user_id: str,
    content_type: str,
    source_type: str,
    title: str,
    summary: str,
    cover_asset_id: str | None,
    cover_url: str,
    tags_json: list[str],
    content_payload: dict,
) -> ContentItem:
    item = ContentItem(
        user_id=user_id,
        content_type=content_type,
        source_type=source_type,
        title=title,
        summary=summary,
        cover_asset_id=cover_asset_id,
        cover_url=cover_url,
        tags_json=tags_json,
        content_payload=content_payload,
    )
    session.add(item)
    session.flush()
    return item


def create_content_media(
    session: Session,
    *,
    content_id: str,
    asset_id: str,
    sort_order: int,
) -> ContentMedia:
    relation = ContentMedia(content_id=content_id, asset_id=asset_id, sort_order=sort_order)
    session.add(relation)
    session.flush()
    return relation


def get_content_with_author(session: Session, content_id: str) -> tuple[ContentItem, User] | None:
    return session.execute(
        select(ContentItem, User).join(User, User.id == ContentItem.user_id).where(ContentItem.id == content_id)
    ).one_or_none()


def list_contents_with_authors(
    session: Session,
    *,
    offset: int,
    limit: int,
    user_id: str | None = None,
) -> list[tuple[ContentItem, User]]:
    query = select(ContentItem, User).join(User, User.id == ContentItem.user_id)
    if user_id is not None:
        query = query.where(ContentItem.user_id == user_id)
    query = query.order_by(ContentItem.published_at.desc(), ContentItem.id.desc()).offset(offset).limit(limit)
    return list(session.execute(query).all())


def count_contents(session: Session, *, user_id: str | None = None) -> int:
    query = select(func.count()).select_from(ContentItem)
    if user_id is not None:
        query = query.where(ContentItem.user_id == user_id)
    return int(session.execute(query).scalar_one())


def get_owned_media_assets_by_ids(session: Session, *, user_id: str, asset_ids: list[str]) -> list[MediaAsset]:
    if not asset_ids:
        return []
    return list(
        session.execute(
            select(MediaAsset)
            .where(
                MediaAsset.user_id == user_id,
                MediaAsset.id.in_(asset_ids),
            )
        ).scalars()
    )
