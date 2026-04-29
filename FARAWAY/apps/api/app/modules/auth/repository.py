from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.auth.model import AuthAccount
from app.modules.users.model import User


def get_account_by_username_key(session: Session, username_key: str) -> AuthAccount | None:
    return session.execute(
        select(AuthAccount).where(AuthAccount.username_key == username_key)
    ).scalar_one_or_none()


def create_user_and_account(
    session: Session,
    *,
    username_raw: str,
    username_key: str,
    password_hash: str,
) -> tuple[User, AuthAccount]:
    user = User(nickname=username_raw, avatar="", bio="", gender="unknown")
    session.add(user)
    session.flush()
    account = AuthAccount(
        user_id=user.id,
        username=username_key,
        username_key=username_key,
        password_hash=password_hash,
        status="active",
    )
    session.add(account)
    session.flush()
    return user, account
