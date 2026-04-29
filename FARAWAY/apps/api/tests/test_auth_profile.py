from __future__ import annotations

import pytest


@pytest.mark.anyio
async def test_auth_profile_and_avatar_flow(client, make_user):
    user = await make_user("Alice_01")

    profile_response = await client.get("/api/user/profile", headers=user["headers"])
    assert profile_response.status_code == 200
    profile = profile_response.json()["data"]
    assert profile["nickname"] == "Alice_01"
    assert profile["gender"] == "unknown"

    upload_response = await client.post(
        "/api/upload/image",
        headers=user["headers"],
        files={"file": ("avatar.png", b"\x89PNG\r\n\x1a\navatar", "image/png")},
    )
    assert upload_response.status_code == 200
    avatar_url = upload_response.json()["data"]["url"]

    update_response = await client.put(
        "/api/user/profile",
        headers=user["headers"],
        json={
            "nickname": "Alice",
            "bio": "探索未知的旅人",
            "avatar": avatar_url,
            "gender": "female",
        },
    )
    assert update_response.status_code == 200
    updated_profile = update_response.json()["data"]
    assert updated_profile["nickname"] == "Alice"
    assert updated_profile["avatar"] == avatar_url
    assert updated_profile["bio"] == "探索未知的旅人"
    assert updated_profile["gender"] == "female"

    public_response = await client.get(f"/api/users/{user['user_id']}", headers=user["headers"])
    assert public_response.status_code == 200
    public_profile = public_response.json()["data"]
    assert public_profile["id"] == user["user_id"]
    assert public_profile["nickname"] == "Alice"

    logout_response = await client.post("/api/auth/logout", headers=user["headers"])
    assert logout_response.status_code == 200
    assert logout_response.json()["data"]["confirmed"] is True
