from __future__ import annotations

import hashlib
import hmac
import secrets
from dataclasses import dataclass
from datetime import timedelta

import jwt
from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.time import utc_now
from app.db.session import get_db


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), bytes.fromhex(salt), 120_000)
    return f"pbkdf2_sha256$120000${salt}${digest.hex()}"


def verify_password(password: str, encoded: str) -> bool:
    try:
        _, iteration_text, salt, digest = encoded.split("$", 3)
    except ValueError:
        return False
    calculated = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        bytes.fromhex(salt),
        int(iteration_text),
    )
    return hmac.compare_digest(calculated.hex(), digest)


def create_access_token(user_id: str) -> str:
    now = utc_now()
    payload = {
        "sub": user_id,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(hours=settings.auth_token_ttl_hours)).timestamp()),
    }
    return jwt.encode(payload, settings.secret_key, algorithm="HS256")


def decode_access_token(token: str) -> str:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
    except jwt.PyJWTError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token") from exc
    user_id = str(payload.get("sub", "")).strip()
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token")
    return user_id


@dataclass(frozen=True)
class CurrentUser:
    id: str


async def get_current_user(
    authorization: str | None = Header(default=None),
    session: Session = Depends(get_db),
) -> CurrentUser:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="missing bearer token")

    from app.modules.users.model import User

    token = authorization.removeprefix("Bearer ").strip()
    user_id = decode_access_token(token)
    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user not found")
    return CurrentUser(id=user_id)


AuthUser = Depends(get_current_user)
