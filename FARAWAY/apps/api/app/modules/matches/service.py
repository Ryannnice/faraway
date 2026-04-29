from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import timedelta

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.constants import (
    ACTIVE_MATCH_REQUEST_STATUSES,
    MatchCandidateStatus,
    MatchDecision,
    MatchPairStatus,
    MatchRequestStatus,
    NotificationType,
)
from app.core.text import normalize_destination, tokenize_preference_text
from app.core.time import (
    build_meet_time,
    deadline_for_request,
    decision_deadline_from,
    ensure_aware,
    has_meet_day_finished,
    overlap_days,
    shanghai_now,
    shanghai_today,
)
from app.core.transactions import managed_transaction
from app.modules.ai.service import generate_meeting_place
from app.modules.matches.model import MatchCandidate, MatchPair, MatchRequest
from app.modules.matches.repository import (
    get_candidate,
    get_latest_request,
    get_pair,
    get_pair_by_pair_key,
    get_request,
    list_closed_history_peer_ids,
    list_pending_candidates_by_pair_key,
    list_pool_requests,
    lock_candidates,
    lock_requests,
)
from app.modules.notifications.service import create_notification_if_missing
from app.modules.users.model import User

logger = logging.getLogger(__name__)


@dataclass
class CandidateScore:
    tag_overlap: int
    keyword_overlap: int
    date_overlap: int


def _conflict(message: str) -> HTTPException:
    return HTTPException(status_code=status.HTTP_409_CONFLICT, detail=message)


def _build_pair_key(request_a_id: str, request_b_id: str) -> str:
    first, second = sorted([request_a_id, request_b_id])
    return f"{first}:{second}"


def _validate_create_payload(payload) -> tuple[str, str, list[str]]:
    destination = normalize_destination(payload.destination)
    if not destination:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="destination is required")
    if payload.travel_end_date < payload.travel_start_date:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="travel_end_date must be >= travel_start_date")
    if payload.travel_start_date < shanghai_today() + timedelta(days=3):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="travel_start_date must be at least 3 days later")
    if not payload.preference_tags and not payload.preference_text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="preference_tags or preference_text must be provided",
        )
    return destination, payload.preference_text.strip(), list(payload.preference_tags)


def _request_is_matchable(request: MatchRequest) -> bool:
    return (
        request.status == MatchRequestStatus.PENDING.value
        and request.current_candidate_id is None
        and request.current_pair_id is None
    )


def _serialize_candidate(candidate: MatchCandidate) -> dict:
    return {
        "candidate_id": candidate.id,
        "peer_user_id": candidate.peer_user_id,
        "peer_nickname": candidate.peer_nickname_snapshot,
        "peer_avatar": candidate.peer_avatar_snapshot,
        "meeting_place_text": candidate.meeting_place_text,
        "match_summary": candidate.match_summary,
        "decision_expires_at": candidate.decision_expires_at,
        "my_decision": candidate.my_decision,
        "peer_decision": candidate.peer_decision,
    }


def _serialize_pair(pair: MatchPair, user_id: str) -> dict:
    if user_id == pair.user_a_id:
        return {
            "pair_id": pair.id,
            "status": pair.status,
            "peer_user_id": pair.user_b_id,
            "peer_nickname": pair.user_b_nickname_snapshot,
            "peer_avatar": pair.user_b_avatar_snapshot,
            "meet_time": pair.meet_time,
            "meet_location_text": pair.meet_location_text,
            "my_remark": pair.remark_a,
            "peer_remark": pair.remark_b,
        }
    return {
        "pair_id": pair.id,
        "status": pair.status,
        "peer_user_id": pair.user_a_id,
        "peer_nickname": pair.user_a_nickname_snapshot,
        "peer_avatar": pair.user_a_avatar_snapshot,
        "meet_time": pair.meet_time,
        "meet_location_text": pair.meet_location_text,
        "my_remark": pair.remark_b,
        "peer_remark": pair.remark_a,
    }


def _serialize_current_state(session: Session, request: MatchRequest | None, user_id: str) -> dict:
    if request is None:
        return {
            "active": False,
            "request_id": None,
            "status": None,
            "candidate": None,
            "pair": None,
        }

    data = {
        "active": request.status in ACTIVE_MATCH_REQUEST_STATUSES,
        "request_id": request.id,
        "status": request.status,
        "destination": request.destination,
        "travel_start_date": request.travel_start_date,
        "travel_end_date": request.travel_end_date,
        "preference_tags": request.preference_tags,
        "preference_text": request.preference_text,
        "match_deadline_at": request.match_deadline_at,
        "candidate": None,
        "pair": None,
    }
    if request.status == MatchRequestStatus.MATCHED_WAITING_DECISION.value and request.current_candidate_id:
        candidate = get_candidate(session, request.current_candidate_id)
        if candidate is not None:
            data["candidate"] = _serialize_candidate(candidate)
    if request.status == MatchRequestStatus.MATCHED_ACCEPTED.value and request.current_pair_id:
        pair = get_pair(session, request.current_pair_id)
        if pair is not None:
            data["pair"] = _serialize_pair(pair, user_id)
    return data


def _match_score(request: MatchRequest, peer_request: MatchRequest) -> CandidateScore:
    request_tags = set(request.preference_tags or [])
    peer_tags = set(peer_request.preference_tags or [])
    request_keywords = tokenize_preference_text(request.preference_text)
    peer_keywords = tokenize_preference_text(peer_request.preference_text)
    return CandidateScore(
        tag_overlap=len(request_tags & peer_tags),
        keyword_overlap=len(request_keywords & peer_keywords),
        date_overlap=overlap_days(
            request.travel_start_date,
            request.travel_end_date,
            peer_request.travel_start_date,
            peer_request.travel_end_date,
        ),
    )


def _build_match_summary(request: MatchRequest, peer_request: MatchRequest) -> str:
    common_tags = list(set(request.preference_tags or []) & set(peer_request.preference_tags or []))
    if common_tags:
        summary = f"你们都偏好{'、'.join(common_tags[:3])}"
        return summary[:40]
    common_keywords = list(
        tokenize_preference_text(request.preference_text) & tokenize_preference_text(peer_request.preference_text)
    )
    if common_keywords:
        summary = f"你们都提到了{common_keywords[0]}"
        return summary[:40]
    return "你们目的地一致，出行时间有重叠"


def _restore_request_state(request: MatchRequest, now) -> None:
    request.current_candidate_id = None
    request.status = (
        MatchRequestStatus.FAILED.value
        if now > ensure_aware(request.match_deadline_at).astimezone(now.tzinfo)
        else MatchRequestStatus.PENDING.value
    )


def _sync_waiting_request(session: Session, request: MatchRequest, now) -> None:
    if not request.current_candidate_id:
        _restore_request_state(request, now)
        return

    locked_candidates = lock_candidates(session, [request.current_candidate_id])
    current_candidate = locked_candidates.get(request.current_candidate_id)
    if current_candidate is None:
        _restore_request_state(request, now)
        return

    peer_candidate = None
    if current_candidate.peer_candidate_id:
        locked_candidates = lock_candidates(session, [current_candidate.id, current_candidate.peer_candidate_id])
        current_candidate = locked_candidates.get(current_candidate.id)
        peer_candidate = locked_candidates.get(current_candidate.peer_candidate_id)

    locked_requests = lock_requests(session, [request.id, current_candidate.peer_request_id])
    current_request = locked_requests.get(request.id, request)
    peer_request = locked_requests.get(current_candidate.peer_request_id)

    if (
        current_candidate.status == MatchCandidateStatus.PENDING_DECISION.value
        and now > ensure_aware(current_candidate.decision_expires_at).astimezone(now.tzinfo)
    ):
        current_candidate.status = MatchCandidateStatus.EXPIRED.value
        if peer_candidate is not None:
            peer_candidate.status = MatchCandidateStatus.EXPIRED.value
        _restore_request_state(current_request, now)
        if peer_request is not None:
            _restore_request_state(peer_request, now)
        return

    if current_candidate.status in {
        MatchCandidateStatus.REJECTED.value,
        MatchCandidateStatus.EXPIRED.value,
    }:
        _restore_request_state(current_request, now)
        if peer_request is not None:
            _restore_request_state(peer_request, now)
        return


def _sync_accepted_request(session: Session, request: MatchRequest, now) -> None:
    if not request.current_pair_id:
        return
    pair = get_pair(session, request.current_pair_id, lock=True)
    if pair is None:
        return
    if pair.status == MatchPairStatus.ACTIVE.value and has_meet_day_finished(pair.meet_time, now):
        locked_requests = lock_requests(session, [pair.request_a_id, pair.request_b_id])
        pair.status = MatchPairStatus.FINISHED.value
        for item in locked_requests.values():
            item.status = MatchRequestStatus.FINISHED.value


def _sync_latest_request(session: Session, user_id: str, *, attempt_match: bool) -> MatchRequest | None:
    request = get_latest_request(session, user_id, lock=True)
    if request is None:
        return None

    now = shanghai_now()
    if request.status == MatchRequestStatus.PENDING.value:
        if now > ensure_aware(request.match_deadline_at).astimezone(now.tzinfo):
            request.status = MatchRequestStatus.FAILED.value
    elif request.status == MatchRequestStatus.MATCHED_WAITING_DECISION.value:
        _sync_waiting_request(session, request, now)
    elif request.status == MatchRequestStatus.MATCHED_ACCEPTED.value:
        _sync_accepted_request(session, request, now)

    session.flush()
    request = get_latest_request(session, user_id, lock=True)
    if attempt_match and request is not None and _request_is_matchable(request):
        _attempt_match(session, request)
        session.flush()
        request = get_latest_request(session, user_id, lock=True)
    return request


def _load_user(session: Session, user_id: str) -> User:
    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    return user


def _attempt_match(session: Session, request: MatchRequest) -> None:
    history_peer_ids = list_closed_history_peer_ids(session, request.id)
    candidates: list[tuple[CandidateScore, MatchRequest]] = []
    for peer_request in list_pool_requests(session, request):
        if peer_request.id in history_peer_ids:
            continue
        if peer_request.current_candidate_id or peer_request.current_pair_id:
            continue
        candidates.append((_match_score(request, peer_request), peer_request))

    candidates.sort(
        key=lambda item: (
            -item[0].tag_overlap,
            -item[0].keyword_overlap,
            -item[0].date_overlap,
            item[1].created_at,
            item[1].id,
        )
    )

    for _, peer_request in candidates:
        locked_requests = lock_requests(session, [request.id, peer_request.id])
        current_request = locked_requests.get(request.id)
        current_peer_request = locked_requests.get(peer_request.id)
        if current_request is None or current_peer_request is None:
            continue
        if not _request_is_matchable(current_request) or not _request_is_matchable(current_peer_request):
            continue

        pair_key = _build_pair_key(current_request.id, current_peer_request.id)
        if get_pair_by_pair_key(session, pair_key, lock=True):
            continue
        if list_pending_candidates_by_pair_key(session, pair_key):
            continue

        current_user = _load_user(session, current_request.user_id)
        peer_user = _load_user(session, current_peer_request.user_id)
        meeting_place = generate_meeting_place(
            current_request.destination,
            list(set(current_request.preference_tags or []) | set(current_peer_request.preference_tags or [])),
            "；".join(
                [item for item in [current_request.preference_text, current_peer_request.preference_text] if item]
            ),
        )
        summary = _build_match_summary(current_request, current_peer_request)
        expires_at = decision_deadline_from()
        candidate = MatchCandidate(
            request_id=current_request.id,
            peer_request_id=current_peer_request.id,
            user_id=current_request.user_id,
            peer_user_id=current_peer_request.user_id,
            peer_nickname_snapshot=peer_user.nickname,
            peer_avatar_snapshot=peer_user.avatar,
            meeting_place_text=meeting_place,
            match_summary=summary,
            my_decision=MatchDecision.PENDING.value,
            peer_decision=MatchDecision.PENDING.value,
            status=MatchCandidateStatus.PENDING_DECISION.value,
            decision_expires_at=expires_at,
            pair_key=pair_key,
        )
        mirror = MatchCandidate(
            request_id=current_peer_request.id,
            peer_request_id=current_request.id,
            user_id=current_peer_request.user_id,
            peer_user_id=current_request.user_id,
            peer_nickname_snapshot=current_user.nickname,
            peer_avatar_snapshot=current_user.avatar,
            meeting_place_text=meeting_place,
            match_summary=summary,
            my_decision=MatchDecision.PENDING.value,
            peer_decision=MatchDecision.PENDING.value,
            status=MatchCandidateStatus.PENDING_DECISION.value,
            decision_expires_at=expires_at,
            pair_key=pair_key,
        )
        session.add(candidate)
        session.add(mirror)
        session.flush()
        candidate.peer_candidate_id = mirror.id
        mirror.peer_candidate_id = candidate.id

        current_request.status = MatchRequestStatus.MATCHED_WAITING_DECISION.value
        current_peer_request.status = MatchRequestStatus.MATCHED_WAITING_DECISION.value
        current_request.current_candidate_id = candidate.id
        current_peer_request.current_candidate_id = mirror.id

        create_notification_if_missing(
            session,
            user_id=current_request.user_id,
            notice_type=NotificationType.REALTIME_MATCH_FOUND.value,
            title="搭子匹配",
            content="系统为你找到了一位新的候选搭子",
            payload={"request_id": current_request.id, "candidate_id": candidate.id},
        )
        create_notification_if_missing(
            session,
            user_id=current_peer_request.user_id,
            notice_type=NotificationType.REALTIME_MATCH_FOUND.value,
            title="搭子匹配",
            content="系统为你找到了一位新的候选搭子",
            payload={"request_id": current_peer_request.id, "candidate_id": mirror.id},
        )
        logger.info(
            "match candidate created pair_key=%s request_a=%s request_b=%s",
            pair_key,
            current_request.id,
            current_peer_request.id,
        )
        return


def create_realtime_request(session: Session, user_id: str, payload) -> dict:
    destination, preference_text, preference_tags = _validate_create_payload(payload)
    with managed_transaction(session):
        latest = _sync_latest_request(session, user_id, attempt_match=False)
        if latest is not None and latest.status == MatchRequestStatus.PENDING.value:
            if latest.current_candidate_id or latest.current_pair_id:
                raise _conflict("pending request can no longer be overwritten")
            latest.status = MatchRequestStatus.CANCELLED.value
            logger.info("match request cancelled by overwrite request_id=%s user_id=%s", latest.id, user_id)
        elif latest is not None and latest.status in {
            MatchRequestStatus.MATCHED_WAITING_DECISION.value,
            MatchRequestStatus.MATCHED_ACCEPTED.value,
        }:
            raise _conflict("active match cannot be replaced")

        new_request = MatchRequest(
            user_id=user_id,
            destination=destination,
            travel_start_date=payload.travel_start_date,
            travel_end_date=payload.travel_end_date,
            preference_tags=preference_tags,
            preference_text=preference_text,
            status=MatchRequestStatus.PENDING.value,
            match_deadline_at=deadline_for_request(payload.travel_start_date),
            current_candidate_id=None,
            current_pair_id=None,
        )
        session.add(new_request)
        session.flush()
        logger.info("match request created request_id=%s user_id=%s", new_request.id, user_id)

        try:
            with session.begin_nested():
                _attempt_match(session, new_request)
        except IntegrityError:
            logger.info("match candidate creation raced request_id=%s user_id=%s", new_request.id, user_id)

        session.flush()
        latest = get_request(session, new_request.id, lock=True)
        return _serialize_current_state(session, latest, user_id)


def get_current_match(session: Session, user_id: str) -> dict:
    with managed_transaction(session):
        latest = _sync_latest_request(session, user_id, attempt_match=True)
        return _serialize_current_state(session, latest, user_id)


def _get_current_candidate_for_user(session: Session, user_id: str, candidate_id: str) -> tuple[MatchCandidate, MatchCandidate, MatchRequest, MatchRequest]:
    latest = _sync_latest_request(session, user_id, attempt_match=False)
    if latest is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="match request not found")

    candidate = get_candidate(session, candidate_id)
    if candidate is None or candidate.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="candidate not found")

    locked_candidates = lock_candidates(session, [candidate.id, candidate.peer_candidate_id or ""])
    candidate = locked_candidates.get(candidate.id)
    peer_candidate = locked_candidates.get(candidate.peer_candidate_id or "") if candidate else None
    if candidate is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="candidate not found")
    if peer_candidate is None:
        raise _conflict("candidate mirror missing")

    locked_requests = lock_requests(session, [candidate.request_id, candidate.peer_request_id])
    request = locked_requests.get(candidate.request_id)
    peer_request = locked_requests.get(candidate.peer_request_id)
    if request is None or peer_request is None:
        raise _conflict("match request not found")
    if latest.id != request.id or request.current_candidate_id != candidate.id:
        raise _conflict("candidate is not current")
    if request.status != MatchRequestStatus.MATCHED_WAITING_DECISION.value:
        raise _conflict("candidate is no longer actionable")
    return candidate, peer_candidate, request, peer_request


def _finalize_pair(
    session: Session,
    *,
    candidate: MatchCandidate,
    peer_candidate: MatchCandidate,
    request: MatchRequest,
    peer_request: MatchRequest,
) -> MatchPair:
    pair_key = _build_pair_key(request.id, peer_request.id)
    pair = get_pair_by_pair_key(session, pair_key, lock=True)
    if pair is None:
        request_a, request_b = sorted([request, peer_request], key=lambda item: item.id)
        user_a = _load_user(session, request_a.user_id)
        user_b = _load_user(session, request_b.user_id)
        pair = MatchPair(
            request_a_id=request_a.id,
            request_b_id=request_b.id,
            user_a_id=request_a.user_id,
            user_b_id=request_b.user_id,
            user_a_nickname_snapshot=user_a.nickname,
            user_b_nickname_snapshot=user_b.nickname,
            user_a_avatar_snapshot=user_a.avatar,
            user_b_avatar_snapshot=user_b.avatar,
            pair_key=pair_key,
            meet_time=build_meet_time(
                request.travel_start_date,
                request.travel_end_date,
                peer_request.travel_start_date,
                peer_request.travel_end_date,
            ),
            meet_location_text=candidate.meeting_place_text,
            remark_a="",
            remark_b="",
            status=MatchPairStatus.ACTIVE.value,
        )
        session.add(pair)
        session.flush()
        logger.info("pair created pair_id=%s pair_key=%s", pair.id, pair_key)

    candidate.status = MatchCandidateStatus.ACCEPTED.value
    peer_candidate.status = MatchCandidateStatus.ACCEPTED.value
    candidate.my_decision = MatchDecision.ACCEPTED.value
    candidate.peer_decision = MatchDecision.ACCEPTED.value
    peer_candidate.my_decision = MatchDecision.ACCEPTED.value
    peer_candidate.peer_decision = MatchDecision.ACCEPTED.value

    request.status = MatchRequestStatus.MATCHED_ACCEPTED.value
    peer_request.status = MatchRequestStatus.MATCHED_ACCEPTED.value
    request.current_candidate_id = None
    peer_request.current_candidate_id = None
    request.current_pair_id = pair.id
    peer_request.current_pair_id = pair.id

    create_notification_if_missing(
        session,
        user_id=request.user_id,
        notice_type=NotificationType.REALTIME_MATCH_CONFIRMED.value,
        title="匹配确认",
        content="你们已经成功确认赴约",
        payload={"request_id": request.id, "pair_id": pair.id},
    )
    create_notification_if_missing(
        session,
        user_id=peer_request.user_id,
        notice_type=NotificationType.REALTIME_MATCH_CONFIRMED.value,
        title="匹配确认",
        content="你们已经成功确认赴约",
        payload={"request_id": peer_request.id, "pair_id": pair.id},
    )
    return pair


def accept_candidate(session: Session, user_id: str, candidate_id: str) -> dict:
    with managed_transaction(session):
        candidate, peer_candidate, request, peer_request = _get_current_candidate_for_user(session, user_id, candidate_id)
        if candidate.status != MatchCandidateStatus.PENDING_DECISION.value:
            raise _conflict("candidate is no longer pending")

        candidate.my_decision = MatchDecision.ACCEPTED.value
        candidate.peer_decision = peer_candidate.my_decision
        peer_candidate.peer_decision = MatchDecision.ACCEPTED.value
        logger.info("candidate accepted candidate_id=%s user_id=%s", candidate.id, user_id)

        if peer_candidate.my_decision == MatchDecision.ACCEPTED.value:
            pair = _finalize_pair(
                session,
                candidate=candidate,
                peer_candidate=peer_candidate,
                request=request,
                peer_request=peer_request,
            )
            return {
                "request_id": request.id,
                "status": MatchRequestStatus.MATCHED_ACCEPTED.value,
                "pair": _serialize_pair(pair, user_id),
            }

        request.status = MatchRequestStatus.MATCHED_WAITING_DECISION.value
        peer_request.status = MatchRequestStatus.MATCHED_WAITING_DECISION.value
        return {
            "request_id": request.id,
            "status": MatchRequestStatus.MATCHED_WAITING_DECISION.value,
            "candidate": _serialize_candidate(candidate),
        }


def reject_candidate(session: Session, user_id: str, candidate_id: str) -> dict:
    with managed_transaction(session):
        candidate, peer_candidate, request, peer_request = _get_current_candidate_for_user(session, user_id, candidate_id)
        if candidate.status != MatchCandidateStatus.PENDING_DECISION.value:
            raise _conflict("candidate is no longer pending")

        candidate.status = MatchCandidateStatus.REJECTED.value
        candidate.my_decision = MatchDecision.REJECTED.value
        candidate.peer_decision = peer_candidate.my_decision
        peer_candidate.status = MatchCandidateStatus.REJECTED.value
        peer_candidate.peer_decision = MatchDecision.REJECTED.value

        now = shanghai_now()
        _restore_request_state(request, now)
        _restore_request_state(peer_request, now)
        logger.info("candidate rejected candidate_id=%s user_id=%s", candidate.id, user_id)
        return {"status": request.status}


def cancel_request(session: Session, user_id: str, request_id: str) -> dict:
    with managed_transaction(session):
        latest = _sync_latest_request(session, user_id, attempt_match=False)
        request = get_request(session, request_id, lock=True)
        if request is None or request.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="match request not found")
        if latest is None or latest.id != request.id:
            raise _conflict("only the latest request can be cancelled")
        if not _request_is_matchable(request):
            raise _conflict("request cannot be cancelled")
        request.status = MatchRequestStatus.CANCELLED.value
        logger.info("match request cancelled request_id=%s user_id=%s", request.id, user_id)
        return {"status": request.status}


def submit_pair_remark(session: Session, user_id: str, pair_id: str, remark: str) -> dict:
    with managed_transaction(session):
        _sync_latest_request(session, user_id, attempt_match=False)
        pair = get_pair(session, pair_id, lock=True)
        if pair is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="pair not found")
        if pair.status != MatchPairStatus.ACTIVE.value:
            raise _conflict("pair already finished")

        if user_id == pair.user_a_id:
            if pair.remark_a:
                raise _conflict("remark already submitted")
            pair.remark_a = remark.strip()
        elif user_id == pair.user_b_id:
            if pair.remark_b:
                raise _conflict("remark already submitted")
            pair.remark_b = remark.strip()
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="forbidden")

        logger.info("pair remark submitted pair_id=%s user_id=%s", pair.id, user_id)
        return _serialize_pair(pair, user_id)
