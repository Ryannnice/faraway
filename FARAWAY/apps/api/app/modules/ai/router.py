from __future__ import annotations

from fastapi import APIRouter, Depends

from app.core.responses import success_response
from app.core.security import CurrentUser, get_current_user
from app.modules.ai.schemas import GenerateStrategyRequest
from app.modules.ai.service import generate_strategy

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/generate-strategy")
async def create_strategy(
    payload: GenerateStrategyRequest,
    current_user: CurrentUser = Depends(get_current_user),
) -> dict:
    del current_user
    return success_response(generate_strategy(payload))
