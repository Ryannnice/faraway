from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.responses import success_response
from app.core.security import CurrentUser, get_current_user
from app.db.session import get_db
from app.modules.users.schemas import UpdateProfileRequest
from app.modules.users.service import get_current_user_profile, get_public_user_profile, update_current_user_profile

router = APIRouter(tags=["users"])


@router.get("/user/profile")
async def read_profile(
    current_user: CurrentUser = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> dict:
    return success_response(get_current_user_profile(session, current_user.id))


@router.put("/user/profile")
async def update_profile(
    payload: UpdateProfileRequest,
    current_user: CurrentUser = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> dict:
    return success_response(update_current_user_profile(session, current_user.id, payload))


@router.get("/users/{user_id}")
async def read_user(
    user_id: str,
    current_user: CurrentUser = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> dict:
    del current_user
    return success_response(get_public_user_profile(session, user_id))
