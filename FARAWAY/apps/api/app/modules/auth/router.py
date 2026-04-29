from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.responses import success_response
from app.core.security import CurrentUser, get_current_user
from app.db.session import get_db
from app.modules.auth.schemas import PasswordLoginRequest, RegisterRequest
from app.modules.auth.service import login_with_password, logout, register_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
async def register(payload: RegisterRequest, session: Session = Depends(get_db)) -> dict:
    return success_response(register_user(session, payload.username, payload.password), message="registered")


@router.post("/password-login")
async def password_login(payload: PasswordLoginRequest, session: Session = Depends(get_db)) -> dict:
    return success_response(login_with_password(session, payload.username, payload.password))


@router.post("/logout")
async def password_logout(current_user: CurrentUser = Depends(get_current_user)) -> dict:
    del current_user
    return success_response(logout())
