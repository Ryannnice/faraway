from __future__ import annotations

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.modules.notifications.model import Notification


def list_recent_notifications(session: Session, user_id: str, limit: int = 50) -> list[Notification]:
    return list(
        session.execute(
            select(Notification)
            .where(Notification.user_id == user_id)
            .order_by(desc(Notification.created_at))
            .limit(limit)
        ).scalars()
    )


def list_notifications_by_type(session: Session, user_id: str, notice_type: str) -> list[Notification]:
    return list(
        session.execute(
            select(Notification).where(Notification.user_id == user_id, Notification.type == notice_type)
        ).scalars()
    )
