from __future__ import annotations

from collections.abc import AsyncGenerator, Callable
from datetime import timedelta
from pathlib import Path

import httpx
import pytest

from app.core.config import settings
from app.core.time import shanghai_today
from app.db.base import Base
import app.db.session as db_session_module
from app.main import app


@pytest.fixture()
async def client(tmp_path: Path) -> AsyncGenerator[httpx.AsyncClient, None]:
    db_path = tmp_path / "test.db"
    media_dir = tmp_path / "uploads"

    settings.database_url = f"sqlite:///{db_path}"
    settings.local_media_dir = str(media_dir)
    settings.dashscope_api_key = ""
    settings.auto_create_schema = False
    media_dir.mkdir(parents=True, exist_ok=True)

    db_session_module.reconfigure_engine(settings.database_url)
    Base.metadata.create_all(bind=db_session_module.engine)

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as async_client:
        yield async_client

    db_session_module.engine.dispose()


@pytest.fixture()
def db_session():
    session = db_session_module.SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def make_user(client: httpx.AsyncClient) -> Callable[[str, str], object]:
    async def _make_user(username: str, password: str = "pass123456") -> dict:
        register_response = await client.post(
            "/api/auth/register",
            json={"username": username, "password": password},
        )
        assert register_response.status_code == 200, register_response.text

        login_response = await client.post(
            "/api/auth/password-login",
            json={"username": username.upper(), "password": password},
        )
        assert login_response.status_code == 200, login_response.text
        data = login_response.json()["data"]
        return {
            "token": data["token"],
            "user_id": data["user_info"]["id"],
            "headers": {"Authorization": f"Bearer {data['token']}"},
        }

    return _make_user


@pytest.fixture()
def make_match_payload() -> Callable[..., dict]:
    def _make_match_payload(
        *,
        destination: str = "大阪",
        start_offset: int = 5,
        duration: int = 3,
        tags: list[str] | None = None,
        text: str = "喜欢白天拍照和美食",
    ) -> dict:
        start = shanghai_today() + timedelta(days=start_offset)
        end = start + timedelta(days=duration - 1)
        return {
            "destination": destination,
            "travel_start_date": start.isoformat(),
            "travel_end_date": end.isoformat(),
            "preference_tags": tags or ["拍照", "美食"],
            "preference_text": text,
        }

    return _make_match_payload
