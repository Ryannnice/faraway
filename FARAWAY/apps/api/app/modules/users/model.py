from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.constants import Gender
from app.core.time import utc_now
from app.db.base import Base


def user_id() -> str:
    from uuid import uuid4

    return f"user_{uuid4().hex[:12]}"


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=user_id)
    nickname: Mapped[str] = mapped_column(String(32), nullable=False)
    avatar: Mapped[str] = mapped_column(String(500), nullable=False, default="")
    bio: Mapped[str] = mapped_column(Text, nullable=False, default="")
    gender: Mapped[str] = mapped_column(String(16), nullable=False, default=Gender.UNKNOWN.value)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
    )
