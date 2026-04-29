from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.transactions import managed_transaction
from app.modules.content.repository import (
    count_contents,
    create_content,
    create_content_media,
    get_content_with_author,
    get_owned_media_assets_by_ids,
    list_contents_with_authors,
)
from app.modules.content.schemas import PublishStrategyRequest, PublishVlogRequest
from app.modules.media.model import MediaAsset
from app.modules.users.model import User

SYSTEM_TAGS = {
    "strategy": "攻略",
    "vlog": "图文",
}


def _truncate(text: str, size: int = 120) -> str:
    value = text.strip()
    if len(value) <= size:
        return value
    return value[:size]


def _serialize_author(user: User) -> dict:
    return {
        "user_id": user.id,
        "nickname": user.nickname,
        "avatar": user.avatar,
    }


def _serialize_tags(content_type: str, tags_json: list[str]) -> list[str]:
    return [SYSTEM_TAGS[content_type], *tags_json]


def _serialize_summary(item, user: User) -> dict:
    return {
        "content_id": item.id,
        "content_type": item.content_type,
        "title": item.title,
        "summary": item.summary,
        "cover_url": item.cover_url,
        "tags": _serialize_tags(item.content_type, item.tags_json),
        "author": _serialize_author(user),
        "published_at": item.published_at,
    }


def _validate_owned_assets(session: Session, *, user_id: str, asset_ids: list[str]) -> list[MediaAsset]:
    if not asset_ids:
        return []
    assets = get_owned_media_assets_by_ids(session, user_id=user_id, asset_ids=asset_ids)
    asset_map = {asset.id: asset for asset in assets}
    if len(asset_map) != len(asset_ids):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="media asset must belong to current user")
    return [asset_map[asset_id] for asset_id in asset_ids]


def _build_pagination_payload(*, items: list[dict], total: int, page: int, page_size: int) -> dict:
    return {
        "list": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "has_more": page * page_size < total,
    }


def publish_strategy(session: Session, user_id: str, payload: PublishStrategyRequest) -> dict:
    cover_assets = _validate_owned_assets(
        session,
        user_id=user_id,
        asset_ids=[payload.cover_asset_id] if payload.cover_asset_id else [],
    )
    cover_asset = cover_assets[0] if cover_assets else None

    with managed_transaction(session):
        item = create_content(
            session,
            user_id=user_id,
            content_type="strategy",
            source_type="ai_strategy",
            title=payload.title,
            summary=_truncate(payload.overview),
            cover_asset_id=cover_asset.id if cover_asset else None,
            cover_url=cover_asset.public_url if cover_asset else "",
            tags_json=payload.tags,
            content_payload={
                "destination": payload.destination,
                "days": payload.days,
                "overview": payload.overview,
                "daily_plans": [plan.model_dump() for plan in payload.daily_plans],
                "tips": payload.tips,
            },
        )
        if cover_asset is not None:
            create_content_media(session, content_id=item.id, asset_id=cover_asset.id, sort_order=0)
        session.flush()

    result = get_content_with_author(session, item.id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="content publish failed")
    return _serialize_summary(result[0], result[1])


def publish_vlog(session: Session, user_id: str, payload: PublishVlogRequest) -> dict:
    assets = _validate_owned_assets(session, user_id=user_id, asset_ids=payload.image_asset_ids)
    cover_asset = assets[0] if assets else None

    with managed_transaction(session):
        item = create_content(
            session,
            user_id=user_id,
            content_type="vlog",
            source_type="manual_vlog",
            title=payload.title,
            summary=_truncate(payload.content),
            cover_asset_id=cover_asset.id if cover_asset else None,
            cover_url=cover_asset.public_url if cover_asset else "",
            tags_json=payload.tags,
            content_payload={
                "content": payload.content,
                "image_asset_ids": [asset.id for asset in assets],
                "image_urls": [asset.public_url for asset in assets],
            },
        )
        for index, asset in enumerate(assets):
            create_content_media(session, content_id=item.id, asset_id=asset.id, sort_order=index)
        session.flush()

    result = get_content_with_author(session, item.id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="content publish failed")
    return _serialize_summary(result[0], result[1])


def get_content_feed(session: Session, *, page: int, page_size: int) -> dict:
    offset = (page - 1) * page_size
    total = count_contents(session)
    rows = list_contents_with_authors(session, offset=offset, limit=page_size)
    items = [_serialize_summary(item, user) for item, user in rows]
    return _build_pagination_payload(items=items, total=total, page=page, page_size=page_size)


def get_my_contents(session: Session, *, user_id: str, page: int, page_size: int) -> dict:
    offset = (page - 1) * page_size
    total = count_contents(session, user_id=user_id)
    rows = list_contents_with_authors(session, offset=offset, limit=page_size, user_id=user_id)
    items = [_serialize_summary(item, user) for item, user in rows]
    return _build_pagination_payload(items=items, total=total, page=page, page_size=page_size)


def get_content_detail(session: Session, content_id: str) -> dict:
    result = get_content_with_author(session, content_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="content not found")

    item, user = result
    detail = _serialize_summary(item, user)
    payload = item.content_payload or {}

    if item.content_type == "strategy":
        detail.update(
            {
                "destination": payload.get("destination", ""),
                "days": payload.get("days", 0),
                "overview": payload.get("overview", ""),
                "daily_plans": payload.get("daily_plans", []),
                "tips": payload.get("tips", []),
            }
        )
        return detail

    detail.update(
        {
            "content": payload.get("content", ""),
            "image_urls": payload.get("image_urls", []),
        }
    )
    return detail
