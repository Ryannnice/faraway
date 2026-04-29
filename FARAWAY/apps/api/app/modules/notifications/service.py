from __future__ import annotations

from sqlalchemy.orm import Session

from app.modules.notifications.model import Notification
from app.modules.notifications.repository import list_notifications_by_type, list_recent_notifications


def build_notice_dedupe_key(notice_type: str, payload: dict) -> str:
    if notice_type == "realtime_match_found":
        return f"{notice_type}:{payload.get('candidate_id', '')}"
    if notice_type == "realtime_match_confirmed":
        return f"{notice_type}:{payload.get('pair_id', '')}"
    return f"{notice_type}:{payload}"


def create_notification_if_missing(
    session: Session,
    *,
    user_id: str,
    notice_type: str,
    title: str,
    content: str,
    payload: dict,
) -> Notification | None:
    dedupe_key = build_notice_dedupe_key(notice_type, payload)
    existing = list_notifications_by_type(session, user_id, notice_type)
    for item in existing:
        if build_notice_dedupe_key(item.type, item.payload or {}) == dedupe_key:
            return None

    notice = Notification(user_id=user_id, type=notice_type, title=title, content=content, payload=payload)
    session.add(notice)
    session.flush()
    return notice


def get_notifications(session: Session, user_id: str) -> dict:
    notices = list_recent_notifications(session, user_id, limit=50)
    return {
        "list": [
            {
                "id": item.id,
                "type": item.type,
                "title": item.title,
                "content": item.content,
                "payload": item.payload,
                "created_at": item.created_at,
                "updated_at": item.updated_at,
            }
            for item in notices
        ]
    }
