from __future__ import annotations

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.core.responses import success_response
from app.core.security import CurrentUser, get_current_user
from app.db.session import get_db
from app.modules.media.service import upload_image

router = APIRouter(prefix="/upload", tags=["media"])


@router.post("/image")
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: CurrentUser = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> dict:
    return success_response(await upload_image(session, current_user.id, file))
