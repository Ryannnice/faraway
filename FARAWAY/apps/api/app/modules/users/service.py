from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.transactions import managed_transaction
from app.modules.users.model import User
from app.modules.users.repository import get_user_by_id, user_owns_media_url
from app.modules.users.schemas import UpdateProfileRequest


def serialize_user_profile(user: User) -> dict:
    return {
        "id": user.id,
        "nickname": user.nickname,
        "avatar": user.avatar,
        "bio": user.bio,
        "gender": user.gender,
        "created_at": user.created_at,
        "updated_at": user.updated_at,
    }


def serialize_user_summary(user: User) -> dict:
    return {
        "id": user.id,
        "nickname": user.nickname,
        "avatar": user.avatar,
        "bio": user.bio,
        "gender": user.gender,
        "created_at": user.created_at,
        "updated_at": user.updated_at,
    }


def get_current_user_profile(session: Session, user_id: str) -> dict:
    user = get_user_by_id(session, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    return serialize_user_profile(user)


def update_current_user_profile(session: Session, user_id: str, payload: UpdateProfileRequest) -> dict:
    with managed_transaction(session):
        user = get_user_by_id(session, user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")

        if payload.nickname is not None:
            user.nickname = payload.nickname
        if payload.bio is not None:
            user.bio = payload.bio
        if payload.gender is not None:
            user.gender = payload.gender
        if payload.avatar is not None:
            if payload.avatar and not user_owns_media_url(session, user_id, payload.avatar):
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="avatar must come from your media asset")
            user.avatar = payload.avatar
        session.add(user)
        session.flush()

    return serialize_user_profile(user)


def get_public_user_profile(session: Session, user_id: str) -> dict:
    user = get_user_by_id(session, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    return serialize_user_summary(user)
