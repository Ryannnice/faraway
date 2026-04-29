from __future__ import annotations

import pytest


PNG_1X1 = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00"
    b"\x1f\x15\xc4\x89\x00\x00\x00\rIDATx\x9cc\xf8\xff\xff?\x00\x05\xfe\x02\xfeA\xd9\x8f\x99\x00"
    b"\x00\x00\x00IEND\xaeB`\x82"
)


async def _upload_image(client, headers, filename: str) -> dict:
    response = await client.post(
        "/api/upload/image",
        headers=headers,
        files={"file": (filename, PNG_1X1, "image/png")},
    )
    assert response.status_code == 200, response.text
    return response.json()["data"]


@pytest.mark.anyio
async def test_publish_content_and_read_feed_detail_and_my_contents(client, make_user):
    user = await make_user("content_owner")

    cover = await _upload_image(client, user["headers"], "cover.png")
    photo_one = await _upload_image(client, user["headers"], "photo-one.png")
    photo_two = await _upload_image(client, user["headers"], "photo-two.png")

    publish_strategy_response = await client.post(
        "/api/content/strategy/publish",
        headers=user["headers"],
        json={
            "title": "京都三天散步攻略",
            "tags": ["赏樱", "慢游"],
            "cover_asset_id": cover["asset_id"],
            "destination": "京都",
            "days": 3,
            "overview": "适合第一次去京都的慢节奏路线。",
            "daily_plans": [
                {"day": 1, "activities": ["清水寺", "祇园"], "food": ["乌冬"], "accommodation": "东山"},
                {"day": 2, "activities": ["岚山"], "food": ["豆腐料理"], "accommodation": "岚山"},
                {"day": 3, "activities": ["伏见稻荷"], "food": ["拉面"], "accommodation": "京都站"},
            ],
            "tips": ["穿舒服的鞋", "热门店要提前排队"],
        },
    )
    assert publish_strategy_response.status_code == 200, publish_strategy_response.text
    published_strategy = publish_strategy_response.json()["data"]
    assert published_strategy["content_type"] == "strategy"
    assert published_strategy["tags"] == ["攻略", "赏樱", "慢游"]
    assert published_strategy["cover_url"] == cover["url"]

    publish_vlog_response = await client.post(
        "/api/content/vlog/publish",
        headers=user["headers"],
        json={
            "title": "京都傍晚散步",
            "content": "把傍晚的街道和小店都走了一遍。",
            "tags": ["夜景"],
            "image_asset_ids": [photo_one["asset_id"], photo_two["asset_id"]],
        },
    )
    assert publish_vlog_response.status_code == 200, publish_vlog_response.text
    published_vlog = publish_vlog_response.json()["data"]
    assert published_vlog["content_type"] == "vlog"
    assert published_vlog["tags"] == ["图文", "夜景"]
    assert published_vlog["cover_url"] == photo_one["url"]

    feed_response = await client.get("/api/content/feed?page=1&page_size=20", headers=user["headers"])
    assert feed_response.status_code == 200, feed_response.text
    feed_data = feed_response.json()["data"]
    assert feed_data["total"] == 2
    assert feed_data["page"] == 1
    assert feed_data["page_size"] == 20
    assert feed_data["has_more"] is False
    assert feed_data["list"][0]["content_id"] == published_vlog["content_id"]
    assert feed_data["list"][1]["content_id"] == published_strategy["content_id"]

    detail_response = await client.get(
        f"/api/content/{published_strategy['content_id']}",
        headers=user["headers"],
    )
    assert detail_response.status_code == 200, detail_response.text
    detail = detail_response.json()["data"]
    assert detail["content_type"] == "strategy"
    assert detail["destination"] == "京都"
    assert len(detail["daily_plans"]) == 3
    assert detail["author"]["user_id"] == user["user_id"]

    my_contents_response = await client.get("/api/my/contents?page=1&page_size=20", headers=user["headers"])
    assert my_contents_response.status_code == 200, my_contents_response.text
    my_contents = my_contents_response.json()["data"]
    assert my_contents["total"] == 2
    assert [item["content_type"] for item in my_contents["list"]] == ["vlog", "strategy"]


@pytest.mark.anyio
async def test_publish_content_rejects_foreign_media(client, make_user):
    owner = await make_user("content_owner_a")
    stranger = await make_user("content_owner_b")

    cover = await _upload_image(client, owner["headers"], "cover.png")

    response = await client.post(
        "/api/content/strategy/publish",
        headers=stranger["headers"],
        json={
            "title": "不应该成功的攻略",
            "tags": ["测试"],
            "cover_asset_id": cover["asset_id"],
            "destination": "京都",
            "days": 1,
            "overview": "这张图不属于我。",
            "daily_plans": [
                {"day": 1, "activities": ["清水寺"], "food": ["乌冬"], "accommodation": "东山"},
            ],
            "tips": [],
        },
    )

    assert response.status_code == 409
    assert response.json()["message"] == "media asset must belong to current user"
