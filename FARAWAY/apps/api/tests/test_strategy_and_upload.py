from __future__ import annotations

import httpx
import pytest

from app.core.config import settings


@pytest.mark.anyio
async def test_generate_strategy_success_and_failure(client, make_user, monkeypatch):
    user = await make_user("planner_01")

    success_response = await client.post(
        "/api/ai/generate-strategy",
        headers=user["headers"],
        json={
            "destination": "京都",
            "days": 3,
            "budget": "中等",
            "hotel_requirement": "",
            "allergies": "",
            "pace": "慢一点",
            "group_type": "自由行",
        },
    )
    assert success_response.status_code == 200
    strategy = success_response.json()["data"]
    assert strategy["destination"] == "京都"
    assert len(strategy["daily_plans"]) == 3
    assert all({"day", "activities", "food", "accommodation"} <= set(day.keys()) for day in strategy["daily_plans"])

    monkeypatch.setattr(settings, "dashscope_api_key", "fake-key")

    class FakeResponse:
        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict:
            return {"choices": [{"message": {"content": '{"destination":"京都","daily_plans":[{"day":1}]}'}}]}

    monkeypatch.setattr(httpx, "post", lambda *args, **kwargs: FakeResponse())

    failure_response = await client.post(
        "/api/ai/generate-strategy",
        headers=user["headers"],
        json={
            "destination": "京都",
            "days": 2,
            "budget": "",
            "hotel_requirement": "",
            "allergies": "",
            "pace": "",
            "group_type": "",
        },
    )
    assert failure_response.status_code == 502
    assert failure_response.json()["message"] == "strategy generation failed"
