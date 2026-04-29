from __future__ import annotations

import httpx
import pytest

from app.core.config import settings


class FakeResponse:
    def __init__(self, content: str) -> None:
        self._content = content

    def raise_for_status(self) -> None:
        return None

    def json(self) -> dict:
        return {"choices": [{"message": {"content": self._content}}]}


@pytest.mark.anyio
async def test_generate_strategy_requires_real_ai_config(client, make_user):
    user = await make_user("planner_missing_key")

    response = await client.post(
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

    assert response.status_code == 503
    assert response.json()["message"] == "dashscope api key missing"


@pytest.mark.anyio
async def test_generate_strategy_success_and_failure_with_mocked_dashscope(client, make_user, monkeypatch):
    user = await make_user("planner_real_ai")
    monkeypatch.setattr(settings, "dashscope_api_key", "fake-key")

    monkeypatch.setattr(
        httpx,
        "post",
        lambda *args, **kwargs: FakeResponse(
            '{"destination":"京都","overview":"三天京都慢游","daily_plans":[{"day":1,"activities":["清水寺"],"food":["乌冬"],"accommodation":"东山"},{"day":2,"activities":["岚山"],"food":["豆腐料理"],"accommodation":"岚山"},{"day":3,"activities":["伏见稻荷"],"food":["拉面"],"accommodation":"京都站"}],"tips":["提前预约热门寺院"]}'
        ),
    )

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
    assert strategy["overview"] == "三天京都慢游"

    monkeypatch.setattr(
        httpx,
        "post",
        lambda *args, **kwargs: FakeResponse('{"destination":"京都","daily_plans":[{"day":1}]}'),
    )

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
    assert failure_response.json()["message"].startswith("dashscope response invalid:")
