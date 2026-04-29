from __future__ import annotations

from enum import Enum


class Gender(str, Enum):
    UNKNOWN = "unknown"
    MALE = "male"
    FEMALE = "female"


class AccountStatus(str, Enum):
    ACTIVE = "active"


class MatchRequestStatus(str, Enum):
    PENDING = "pending"
    MATCHED_WAITING_DECISION = "matched_waiting_decision"
    MATCHED_ACCEPTED = "matched_accepted"
    FAILED = "failed"
    CANCELLED = "cancelled"
    FINISHED = "finished"


class MatchCandidateStatus(str, Enum):
    PENDING_DECISION = "pending_decision"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    EXPIRED = "expired"


class MatchDecision(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class MatchPairStatus(str, Enum):
    ACTIVE = "active"
    FINISHED = "finished"


class NotificationType(str, Enum):
    REALTIME_MATCH_FOUND = "realtime_match_found"
    REALTIME_MATCH_CONFIRMED = "realtime_match_confirmed"


ACTIVE_MATCH_REQUEST_STATUSES = {
    MatchRequestStatus.PENDING.value,
    MatchRequestStatus.MATCHED_WAITING_DECISION.value,
    MatchRequestStatus.MATCHED_ACCEPTED.value,
}

TERMINAL_MATCH_REQUEST_STATUSES = {
    MatchRequestStatus.FAILED.value,
    MatchRequestStatus.CANCELLED.value,
    MatchRequestStatus.FINISHED.value,
}

PREFERENCE_TAGS = [
    "特种兵",
    "慢旅行",
    "拍照",
    "美食",
    "自然风光",
    "人文历史",
    "早起",
    "夜景",
]

ALLOWED_IMAGE_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}
