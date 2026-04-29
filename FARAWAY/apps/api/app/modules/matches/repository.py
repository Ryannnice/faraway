from __future__ import annotations

from collections.abc import Iterable

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.constants import MatchCandidateStatus, MatchRequestStatus
from app.modules.matches.model import MatchCandidate, MatchPair, MatchRequest


def get_latest_request(session: Session, user_id: str, *, lock: bool = False) -> MatchRequest | None:
    stmt = (
        select(MatchRequest)
        .where(MatchRequest.user_id == user_id)
        .order_by(desc(MatchRequest.created_at), desc(MatchRequest.id))
        .limit(1)
    )
    if lock:
        stmt = stmt.with_for_update()
    return session.execute(stmt).scalar_one_or_none()


def get_request(session: Session, request_id: str, *, lock: bool = False) -> MatchRequest | None:
    stmt = select(MatchRequest).where(MatchRequest.id == request_id)
    if lock:
        stmt = stmt.with_for_update()
    return session.execute(stmt).scalar_one_or_none()


def get_candidate(session: Session, candidate_id: str, *, lock: bool = False) -> MatchCandidate | None:
    stmt = select(MatchCandidate).where(MatchCandidate.id == candidate_id)
    if lock:
        stmt = stmt.with_for_update()
    return session.execute(stmt).scalar_one_or_none()


def get_pair(session: Session, pair_id: str, *, lock: bool = False) -> MatchPair | None:
    stmt = select(MatchPair).where(MatchPair.id == pair_id)
    if lock:
        stmt = stmt.with_for_update()
    return session.execute(stmt).scalar_one_or_none()


def get_pair_by_pair_key(session: Session, pair_key: str, *, lock: bool = False) -> MatchPair | None:
    stmt = select(MatchPair).where(MatchPair.pair_key == pair_key)
    if lock:
        stmt = stmt.with_for_update()
    return session.execute(stmt).scalar_one_or_none()


def list_pool_requests(session: Session, request: MatchRequest) -> list[MatchRequest]:
    stmt = (
        select(MatchRequest)
        .where(
            MatchRequest.status == MatchRequestStatus.PENDING.value,
            MatchRequest.destination == request.destination,
            MatchRequest.travel_start_date <= request.travel_end_date,
            MatchRequest.travel_end_date >= request.travel_start_date,
            MatchRequest.user_id != request.user_id,
        )
        .order_by(MatchRequest.created_at.asc(), MatchRequest.id.asc())
        .limit(settings.match_candidate_slice_size)
    )
    return list(session.execute(stmt).scalars())


def list_closed_history_peer_ids(session: Session, request_id: str) -> set[str]:
    stmt = select(MatchCandidate.peer_request_id).where(
        MatchCandidate.request_id == request_id,
        MatchCandidate.status.in_(
            [MatchCandidateStatus.REJECTED.value, MatchCandidateStatus.EXPIRED.value]
        ),
    )
    return {item for item in session.execute(stmt).scalars()}


def list_pending_candidates_by_pair_key(session: Session, pair_key: str) -> list[MatchCandidate]:
    stmt = select(MatchCandidate).where(
        MatchCandidate.pair_key == pair_key,
        MatchCandidate.status == MatchCandidateStatus.PENDING_DECISION.value,
    )
    return list(session.execute(stmt).scalars())


def lock_requests(session: Session, request_ids: Iterable[str]) -> dict[str, MatchRequest]:
    ids = sorted({item for item in request_ids if item})
    if not ids:
        return {}
    stmt = select(MatchRequest).where(MatchRequest.id.in_(ids)).order_by(MatchRequest.id.asc()).with_for_update()
    return {item.id: item for item in session.execute(stmt).scalars()}


def lock_candidates(session: Session, candidate_ids: Iterable[str]) -> dict[str, MatchCandidate]:
    ids = sorted({item for item in candidate_ids if item})
    if not ids:
        return {}
    stmt = select(MatchCandidate).where(MatchCandidate.id.in_(ids)).order_by(MatchCandidate.id.asc()).with_for_update()
    return {item.id: item for item in session.execute(stmt).scalars()}
