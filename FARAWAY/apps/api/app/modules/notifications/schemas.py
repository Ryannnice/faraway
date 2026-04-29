from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class NotificationItem(BaseModel):
    id: str
    type: str
    title: str
    content: str
    payload: dict
    created_at: datetime
    updated_at: datetime


class NotificationListResponse(BaseModel):
    list: list[NotificationItem]
