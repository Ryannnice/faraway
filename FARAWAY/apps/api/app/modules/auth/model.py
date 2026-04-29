from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.constants import AccountStatus
from app.core.time import utc_now
from app.db.base import Base


def auth_account_id() -> str:
    from uuid import uuid4

    return f"acct_{uuid4().hex[:12]}"


class AuthAccount(Base):
    __tablename__ = "auth_accounts"

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=auth_account_id)
    user_id: Mapped[str] = mapped_column(String(32), ForeignKey("users.id"), nullable=False, unique=True)
    username: Mapped[str] = mapped_column(String(32), nullable=False)
    username_key: Mapped[str] = mapped_column(String(32), nullable=False, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default=AccountStatus.ACTIVE.value)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
    )
