from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.responses import success_response
from app.core.security import CurrentUser, get_current_user
from app.db.session import get_db
from app.modules.notifications.service import get_notifications

router = APIRouter(prefix="/my", tags=["notifications"])


@router.get("/notifications")
async def list_notifications(
    current_user: CurrentUser = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> dict:
    return success_response(get_notifications(session, current_user.id))
