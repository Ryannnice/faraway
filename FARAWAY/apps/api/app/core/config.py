from __future__ import annotations

import json
from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]
ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):
    app_name: str = "Faraway API"
    environment: str = "development"
    api_prefix: str = "/api"
    secret_key: str = "change-me"
    auth_token_ttl_hours: int = 24 * 30
    database_url: str = "sqlite:///./data/faraway.db"
    cors_origins: list[str] = Field(default_factory=lambda: ["*"])
    auto_create_schema: bool = True

    timezone_name: str = "Asia/Shanghai"
    match_candidate_slice_size: int = 50
    poll_interval_seconds: int = 5
    decision_expire_minutes: int = 15
    meet_hour: int = 10

    dashscope_api_key: str = ""
    dashscope_base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    dashscope_model: str = "qwen-plus"
    strategy_ai_timeout_seconds: int = 20
    meeting_place_ai_timeout_seconds: int = 3

    oss_access_key_id: str = ""
    oss_access_key_secret: str = ""
    oss_endpoint: str = "https://oss-cn-hangzhou.aliyuncs.com"
    oss_bucket_name: str = ""
    oss_public_base_url: str = ""
    local_media_dir: str = "data/uploads"
    local_media_url_prefix: str = "/media"

    max_image_size_mb: int = 10

    model_config = SettingsConfigDict(env_file=ENV_FILE, env_file_encoding="utf-8", extra="ignore")

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: object) -> list[str]:
        if isinstance(value, list):
            return [str(item) for item in value]
        if isinstance(value, str):
            text = value.strip()
            if not text:
                return ["*"]
            if text.startswith("["):
                return [str(item) for item in json.loads(text)]
            return [item.strip() for item in text.split(",") if item.strip()]
        return ["*"]

    @property
    def resolved_local_media_dir(self) -> Path:
        path = Path(self.local_media_dir)
        if path.is_absolute():
            return path
        return (BASE_DIR / path).resolve()

    @property
    def media_url_prefix(self) -> str:
        prefix = self.local_media_url_prefix.strip()
        if not prefix:
            return "/media"
        return prefix if prefix.startswith("/") else f"/{prefix}"

    @property
    def oss_enabled(self) -> bool:
        return all(
            [
                self.oss_access_key_id,
                self.oss_access_key_secret,
                self.oss_endpoint,
                self.oss_bucket_name,
            ]
        )


settings = Settings()
