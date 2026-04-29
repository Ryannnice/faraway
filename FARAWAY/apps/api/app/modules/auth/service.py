from __future__ import annotations

import logging

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.constants import AccountStatus
from app.core.security import create_access_token, hash_password, verify_password
from app.core.text import normalize_username
from app.core.transactions import managed_transaction
from app.modules.auth.repository import create_user_and_account, get_account_by_username_key
from app.modules.users.schemas import UserProfileResponse, UserSummaryResponse

logger = logging.getLogger(__name__)


def register_user(session: Session, username: str, password: str) -> dict:
    username_key = normalize_username(username)
    try:
        with managed_transaction(session):
            if get_account_by_username_key(session, username_key):
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="username already exists")
            user, account = create_user_and_account(
                session,
                username_raw=username,
                username_key=username_key,
                password_hash=hash_password(password),
            )
            logger.info("register success username=%s user_id=%s", account.username_key, user.id)
    except IntegrityError as exc:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="username already exists") from exc

    return {
        "id": user.id,
        "username": account.username,
        "nickname": user.nickname,
        "avatar": user.avatar,
        "bio": user.bio,
        "gender": user.gender,
        "created_at": user.created_at,
    }


def login_with_password(session: Session, username: str, password: str) -> dict:
    username_key = normalize_username(username)
    account = get_account_by_username_key(session, username_key)
    if account is None or account.status != AccountStatus.ACTIVE.value or not verify_password(password, account.password_hash):
        logger.info("login failed username=%s", username_key)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid username or password")

    from app.modules.users.model import User

    user = session.get(User, account.user_id)
    if user is None:
        logger.info("login failed username=%s missing user", username_key)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid username or password")

    logger.info("login success username=%s user_id=%s", username_key, user.id)
    return {
        "token": create_access_token(user.id),
        "user_info": UserSummaryResponse.model_validate(user).model_dump(),
    }


def logout() -> dict:
    return {"confirmed": True}
