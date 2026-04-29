from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import JSON, Date, DateTime, ForeignKey, Index, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.time import utc_now
from app.db.base import Base


def match_request_id() -> str:
    from uuid import uuid4

    return f"req_{uuid4().hex[:12]}"


def match_candidate_id() -> str:
    from uuid import uuid4

    return f"cand_{uuid4().hex[:12]}"


def match_pair_id() -> str:
    from uuid import uuid4

    return f"pair_{uuid4().hex[:12]}"


ACTIVE_REQUESTS_SQL = text("status in ('pending', 'matched_waiting_decision', 'matched_accepted')")


class MatchRequest(Base):
    __tablename__ = "match_requests"
    __table_args__ = (
        Index(
            "uq_match_requests_active_user",
            "user_id",
            unique=True,
            sqlite_where=ACTIVE_REQUESTS_SQL,
            postgresql_where=ACTIVE_REQUESTS_SQL,
        ),
        Index(
            "ix_match_requests_pool_lookup",
            "status",
            "destination",
            "travel_start_date",
            "travel_end_date",
            "created_at",
        ),
    )

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=match_request_id)
    user_id: Mapped[str] = mapped_column(String(32), ForeignKey("users.id"), nullable=False, index=True)
    destination: Mapped[str] = mapped_column(String(100), nullable=False)
    travel_start_date: Mapped[date] = mapped_column(Date, nullable=False)
    travel_end_date: Mapped[date] = mapped_column(Date, nullable=False)
    preference_tags: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    preference_text: Mapped[str] = mapped_column(Text, nullable=False, default="")
    status: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    match_deadline_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    current_candidate_id: Mapped[str | None] = mapped_column(String(32), ForeignKey("match_candidates.id"), nullable=True)
    current_pair_id: Mapped[str | None] = mapped_column(String(32), ForeignKey("match_pairs.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
    )


class MatchCandidate(Base):
    __tablename__ = "match_candidates"
    __table_args__ = (
        Index("uq_match_candidates_request_peer", "request_id", "peer_request_id", unique=True),
        Index("uq_match_candidates_peer_candidate_id", "peer_candidate_id", unique=True),
        Index("ix_match_candidates_pair_key", "pair_key"),
    )

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=match_candidate_id)
    request_id: Mapped[str] = mapped_column(String(32), ForeignKey("match_requests.id"), nullable=False, index=True)
    peer_request_id: Mapped[str] = mapped_column(String(32), ForeignKey("match_requests.id"), nullable=False, index=True)
    user_id: Mapped[str] = mapped_column(String(32), ForeignKey("users.id"), nullable=False, index=True)
    peer_user_id: Mapped[str] = mapped_column(String(32), ForeignKey("users.id"), nullable=False, index=True)
    peer_nickname_snapshot: Mapped[str] = mapped_column(String(32), nullable=False)
    peer_avatar_snapshot: Mapped[str] = mapped_column(String(500), nullable=False, default="")
    meeting_place_text: Mapped[str] = mapped_column(String(200), nullable=False)
    match_summary: Mapped[str] = mapped_column(String(40), nullable=False)
    my_decision: Mapped[str] = mapped_column(String(16), nullable=False, default="pending")
    peer_decision: Mapped[str] = mapped_column(String(16), nullable=False, default="pending")
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="pending_decision", index=True)
    decision_expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    pair_key: Mapped[str] = mapped_column(String(80), nullable=False)
    peer_candidate_id: Mapped[str | None] = mapped_column(String(32), ForeignKey("match_candidates.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
    )


class MatchPair(Base):
    __tablename__ = "match_pairs"
    __table_args__ = (Index("uq_match_pairs_pair_key", "pair_key", unique=True),)

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=match_pair_id)
    request_a_id: Mapped[str] = mapped_column(String(32), ForeignKey("match_requests.id"), nullable=False)
    request_b_id: Mapped[str] = mapped_column(String(32), ForeignKey("match_requests.id"), nullable=False)
    user_a_id: Mapped[str] = mapped_column(String(32), ForeignKey("users.id"), nullable=False)
    user_b_id: Mapped[str] = mapped_column(String(32), ForeignKey("users.id"), nullable=False)
    user_a_nickname_snapshot: Mapped[str] = mapped_column(String(32), nullable=False)
    user_b_nickname_snapshot: Mapped[str] = mapped_column(String(32), nullable=False)
    user_a_avatar_snapshot: Mapped[str] = mapped_column(String(500), nullable=False, default="")
    user_b_avatar_snapshot: Mapped[str] = mapped_column(String(500), nullable=False, default="")
    pair_key: Mapped[str] = mapped_column(String(80), nullable=False)
    meet_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    meet_location_text: Mapped[str] = mapped_column(String(200), nullable=False)
    remark_a: Mapped[str] = mapped_column(String(200), nullable=False, default="")
    remark_b: Mapped[str] = mapped_column(String(200), nullable=False, default="")
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="active")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
    )
