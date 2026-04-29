from __future__ import annotations

import asyncio
from datetime import timedelta

import httpx
import pytest
from sqlalchemy import func, select

from app.core.time import ensure_aware, shanghai_now
import app.db.session as db_session_module
from app.main import app
from app.modules.matches.model import MatchCandidate, MatchPair, MatchRequest


async def _create_pairing(client, user_a, user_b, payload):
    response_a = await client.post("/api/match/realtime", headers=user_a["headers"], json=payload)
    assert response_a.status_code == 200, response_a.text
    response_b = await client.post("/api/match/realtime", headers=user_b["headers"], json=payload)
    assert response_b.status_code == 200, response_b.text

    current_a = (await client.get("/api/match/realtime/current", headers=user_a["headers"])).json()["data"]
    current_b = (await client.get("/api/match/realtime/current", headers=user_b["headers"])).json()["data"]
    return current_a, current_b


async def _post_with_new_client(path: str, *, headers: dict, json: dict | None = None) -> httpx.Response:
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as async_client:
        return await async_client.post(path, headers=headers, json=json)


@pytest.mark.anyio
async def test_match_request_replace_cancel_and_terminal_state(client, db_session, make_user, make_match_payload):
    user = await make_user("matcher_01")

    first_payload = make_match_payload(text="偏好美食和拍照")
    first_response = await client.post("/api/match/realtime", headers=user["headers"], json=first_payload)
    assert first_response.status_code == 200
    first_data = first_response.json()["data"]
    assert first_data["status"] == "pending"

    second_payload = make_match_payload(text="喜欢自然风光", tags=["自然风光"])
    second_response = await client.post("/api/match/realtime", headers=user["headers"], json=second_payload)
    assert second_response.status_code == 200
    second_data = second_response.json()["data"]
    assert second_data["status"] == "pending"

    requests = list(db_session.execute(select(MatchRequest).order_by(MatchRequest.created_at.asc())).scalars())
    assert [item.status for item in requests] == ["cancelled", "pending"]

    cancel_response = await client.post(
        f"/api/match/realtime/{second_data['request_id']}/cancel",
        headers=user["headers"],
    )
    assert cancel_response.status_code == 200
    assert cancel_response.json()["data"]["status"] == "cancelled"

    current_response = await client.get("/api/match/realtime/current", headers=user["headers"])
    assert current_response.status_code == 200
    current_data = current_response.json()["data"]
    assert current_data["active"] is False
    assert current_data["status"] == "cancelled"
    assert current_data["destination"] == "大阪"


@pytest.mark.anyio
async def test_match_reject_flow_and_found_notifications(client, make_user, make_match_payload):
    user_a = await make_user("alice_match")
    user_b = await make_user("bob_match")
    payload = make_match_payload()

    current_a, current_b = await _create_pairing(client, user_a, user_b, payload)
    assert current_a["status"] == "matched_waiting_decision"
    assert current_b["status"] == "matched_waiting_decision"

    notices_a = (await client.get("/api/my/notifications", headers=user_a["headers"])).json()["data"]["list"]
    notices_b = (await client.get("/api/my/notifications", headers=user_b["headers"])).json()["data"]["list"]
    assert [item["type"] for item in notices_a] == ["realtime_match_found"]
    assert [item["type"] for item in notices_b] == ["realtime_match_found"]

    reject_response = await client.post(
        f"/api/match/realtime/candidate/{current_a['candidate']['candidate_id']}/reject",
        headers=user_a["headers"],
    )
    assert reject_response.status_code == 200
    assert reject_response.json()["data"]["status"] == "pending"

    current_b_after = (await client.get("/api/match/realtime/current", headers=user_b["headers"])).json()["data"]
    assert current_b_after["status"] == "pending"


@pytest.mark.anyio
async def test_match_accept_confirm_remark_and_lazy_finish(client, db_session, make_user, make_match_payload):
    user_a = await make_user("confirm_a")
    user_b = await make_user("confirm_b")
    payload = make_match_payload()

    current_a, current_b = await _create_pairing(client, user_a, user_b, payload)

    accept_a = await client.post(
        f"/api/match/realtime/candidate/{current_a['candidate']['candidate_id']}/accept",
        headers=user_a["headers"],
    )
    assert accept_a.status_code == 200
    waiting_state = accept_a.json()["data"]
    assert waiting_state["status"] == "matched_waiting_decision"
    assert waiting_state["candidate"]["my_decision"] == "accepted"
    assert waiting_state["candidate"]["peer_decision"] == "pending"

    accept_b = await client.post(
        f"/api/match/realtime/candidate/{current_b['candidate']['candidate_id']}/accept",
        headers=user_b["headers"],
    )
    assert accept_b.status_code == 200
    accepted_state = accept_b.json()["data"]
    assert accepted_state["status"] == "matched_accepted"
    pair_id = accepted_state["pair"]["pair_id"]

    notices_a = (await client.get("/api/my/notifications", headers=user_a["headers"])).json()["data"]["list"]
    notices_b = (await client.get("/api/my/notifications", headers=user_b["headers"])).json()["data"]["list"]
    assert [item["type"] for item in notices_a] == ["realtime_match_confirmed", "realtime_match_found"]
    assert [item["type"] for item in notices_b] == ["realtime_match_confirmed", "realtime_match_found"]

    remark_response = await client.post(
        f"/api/match/realtime/pair/{pair_id}/remark",
        headers=user_a["headers"],
        json={"remark": "我会背黑色双肩包，提前 10 分钟到。"},
    )
    assert remark_response.status_code == 200
    assert remark_response.json()["data"]["my_remark"] == "我会背黑色双肩包，提前 10 分钟到。"

    second_remark = await client.post(
        f"/api/match/realtime/pair/{pair_id}/remark",
        headers=user_a["headers"],
        json={"remark": "再次修改"},
    )
    assert second_remark.status_code == 409

    current_b_after = (await client.get("/api/match/realtime/current", headers=user_b["headers"])).json()["data"]
    assert current_b_after["pair"]["peer_remark"] == "我会背黑色双肩包，提前 10 分钟到。"

    pair = db_session.execute(select(MatchPair).where(MatchPair.id == pair_id)).scalar_one()
    pair.meet_time = shanghai_now() - timedelta(days=2)
    db_session.add(pair)
    db_session.commit()

    finished_response = await client.get("/api/match/realtime/current", headers=user_a["headers"])
    assert finished_response.status_code == 200
    finished_state = finished_response.json()["data"]
    assert finished_state["active"] is False
    assert finished_state["status"] == "finished"


@pytest.mark.anyio
async def test_simultaneous_accept_creates_single_pair(client, make_user, make_match_payload):
    user_a = await make_user("race_accept_a")
    user_b = await make_user("race_accept_b")
    payload = make_match_payload()
    current_a, current_b = await _create_pairing(client, user_a, user_b, payload)
    candidate_a = current_a["candidate"]["candidate_id"]
    candidate_b = current_b["candidate"]["candidate_id"]

    responses = await asyncio.gather(
        _post_with_new_client(
            f"/api/match/realtime/candidate/{candidate_a}/accept",
            headers=user_a["headers"],
        ),
        _post_with_new_client(
            f"/api/match/realtime/candidate/{candidate_b}/accept",
            headers=user_b["headers"],
        ),
    )
    assert all(response.status_code == 200 for response in responses)

    with db_session_module.SessionLocal() as session:
        pair_count = session.execute(select(func.count()).select_from(MatchPair)).scalar_one()
        assert pair_count == 1

    current_a_after = (await client.get("/api/match/realtime/current", headers=user_a["headers"])).json()["data"]
    current_b_after = (await client.get("/api/match/realtime/current", headers=user_b["headers"])).json()["data"]
    assert current_a_after["status"] == "matched_accepted"
    assert current_b_after["status"] == "matched_accepted"


@pytest.mark.anyio
async def test_simultaneous_create_produces_single_candidate_group(client, make_user, make_match_payload):
    user_a = await make_user("race_create_a")
    user_b = await make_user("race_create_b")
    payload = make_match_payload()

    responses = await asyncio.gather(
        _post_with_new_client("/api/match/realtime", headers=user_a["headers"], json=payload),
        _post_with_new_client("/api/match/realtime", headers=user_b["headers"], json=payload),
    )
    assert all(response.status_code == 200 for response in responses)

    with db_session_module.SessionLocal() as session:
        candidate_count = session.execute(select(func.count()).select_from(MatchCandidate)).scalar_one()
        assert candidate_count == 2

    current_a = (await client.get("/api/match/realtime/current", headers=user_a["headers"])).json()["data"]
    current_b = (await client.get("/api/match/realtime/current", headers=user_b["headers"])).json()["data"]
    assert current_a["status"] == "matched_waiting_decision"
    assert current_b["status"] == "matched_waiting_decision"
