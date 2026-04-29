from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.responses import success_response
from app.core.security import CurrentUser, get_current_user
from app.db.session import get_db
from app.modules.matches.schemas import CreateRealtimeMatchRequest, SubmitRemarkRequest
from app.modules.matches.service import (
    accept_candidate,
    cancel_request,
    create_realtime_request,
    get_current_match,
    reject_candidate,
    submit_pair_remark,
)

router = APIRouter(prefix="/match/realtime", tags=["matches"])


@router.post("")
async def create_match(
    payload: CreateRealtimeMatchRequest,
    current_user: CurrentUser = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> dict:
    return success_response(create_realtime_request(session, current_user.id, payload))


@router.get("/current")
async def read_current_match(
    current_user: CurrentUser = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> dict:
    return success_response(get_current_match(session, current_user.id))


@router.post("/candidate/{candidate_id}/accept")
async def accept_match_candidate(
    candidate_id: str,
    current_user: CurrentUser = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> dict:
    return success_response(accept_candidate(session, current_user.id, candidate_id))


@router.post("/candidate/{candidate_id}/reject")
async def reject_match_candidate(
    candidate_id: str,
    current_user: CurrentUser = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> dict:
    return success_response(reject_candidate(session, current_user.id, candidate_id))


@router.post("/pair/{pair_id}/remark")
async def remark_match_pair(
    pair_id: str,
    payload: SubmitRemarkRequest,
    current_user: CurrentUser = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> dict:
    return success_response(submit_pair_remark(session, current_user.id, pair_id, payload.remark))


@router.post("/{request_id}/cancel")
async def cancel_match_request(
    request_id: str,
    current_user: CurrentUser = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> dict:
    return success_response(cancel_request(session, current_user.id, request_id))
