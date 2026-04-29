from __future__ import annotations

from datetime import datetime

from sqlalchemy import JSON, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.time import utc_now
from app.db.base import Base


def content_id() -> str:
    from uuid import uuid4

    return f"cnt_{uuid4().hex[:12]}"


def content_media_id() -> str:
    from uuid import uuid4

    return f"cntm_{uuid4().hex[:12]}"


class ContentItem(Base):
    __tablename__ = "contents"

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=content_id)
    user_id: Mapped[str] = mapped_column(String(32), ForeignKey("users.id"), nullable=False, index=True)
    content_type: Mapped[str] = mapped_column(String(16), nullable=False, index=True)
    source_type: Mapped[str] = mapped_column(String(32), nullable=False)
    title: Mapped[str] = mapped_column(String(60), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    cover_asset_id: Mapped[str | None] = mapped_column(String(32), ForeignKey("media_assets.id"), nullable=True)
    cover_url: Mapped[str] = mapped_column(String(500), nullable=False, default="")
    tags_json: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    content_payload: Mapped[dict] = mapped_column(JSON, nullable=False)
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utc_now, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
    )


class ContentMedia(Base):
    __tablename__ = "content_media"

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=content_media_id)
    content_id: Mapped[str] = mapped_column(String(32), ForeignKey("contents.id"), nullable=False, index=True)
    asset_id: Mapped[str] = mapped_column(String(32), ForeignKey("media_assets.id"), nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utc_now)
