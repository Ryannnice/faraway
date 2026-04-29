from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.responses import success_response
from app.core.security import CurrentUser, get_current_user
from app.db.session import get_db
from app.modules.content.schemas import PublishStrategyRequest, PublishVlogRequest
from app.modules.content.service import get_content_detail, get_content_feed, get_my_contents, publish_strategy, publish_vlog

router = APIRouter(tags=["content"])


@router.post("/content/strategy/publish")
async def create_strategy_content(
    payload: PublishStrategyRequest,
    current_user: CurrentUser = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> dict:
    return success_response(publish_strategy(session, current_user.id, payload))


@router.post("/content/vlog/publish")
async def create_vlog_content(
    payload: PublishVlogRequest,
    current_user: CurrentUser = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> dict:
    return success_response(publish_vlog(session, current_user.id, payload))


@router.get("/content/feed")
async def read_content_feed(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=50),
    current_user: CurrentUser = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> dict:
    del current_user
    return success_response(get_content_feed(session, page=page, page_size=page_size))


@router.get("/content/{content_id}")
async def read_content_detail(
    content_id: str,
    current_user: CurrentUser = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> dict:
    del current_user
    return success_response(get_content_detail(session, content_id))


@router.get("/my/contents")
async def read_my_contents(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=50),
    current_user: CurrentUser = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> dict:
    return success_response(get_my_contents(session, user_id=current_user.id, page=page, page_size=page_size))
