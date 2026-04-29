from __future__ import annotations

from datetime import date, datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo

from app.core.config import settings

UTC = timezone.utc
SHANGHAI = ZoneInfo(settings.timezone_name)


def utc_now() -> datetime:
    return datetime.now(UTC)


def shanghai_now() -> datetime:
    return utc_now().astimezone(SHANGHAI)


def ensure_aware(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value.astimezone(UTC)


def shanghai_today() -> date:
    return shanghai_now().date()


def deadline_for_request(travel_start_date: date) -> datetime:
    start_day_end = datetime.combine(travel_start_date, time(23, 59, 59), tzinfo=SHANGHAI)
    return start_day_end - timedelta(hours=48)


def decision_deadline_from(now: datetime | None = None) -> datetime:
    current = now or shanghai_now()
    return current.astimezone(SHANGHAI) + timedelta(minutes=settings.decision_expire_minutes)


def overlap_days(a_start: date, a_end: date, b_start: date, b_end: date) -> int:
    start = max(a_start, b_start)
    end = min(a_end, b_end)
    if end < start:
        return 0
    return (end - start).days + 1


def build_meet_time(a_start: date, a_end: date, b_start: date, b_end: date) -> datetime:
    meet_day = max(a_start, b_start)
    if meet_day > min(a_end, b_end):
        raise ValueError("match requests do not overlap")
    return datetime.combine(meet_day, time(settings.meet_hour, 0), tzinfo=SHANGHAI)


def has_meet_day_finished(meet_time: datetime, now: datetime | None = None) -> bool:
    current = (now or shanghai_now()).astimezone(SHANGHAI)
    meet_local = ensure_aware(meet_time).astimezone(SHANGHAI)
    end_of_day = datetime.combine(meet_local.date(), time(23, 59, 59), tzinfo=SHANGHAI)
    return current > end_of_day
