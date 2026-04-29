from __future__ import annotations

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]
ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):
    app_name: str = "Faraway Backend"
    environment: str = "development"
    dev_allow_anon_auth: bool = False
    dev_trust_x_user_headers: bool = False
    secret_key: str = "change-this-in-production-please-use-a-long-random-secret-key"
    sqlite_path: str = "data/faraway_app.db"
    sqlite_journal_mode: str = "MEMORY"
    cors_origins: list[str] = Field(default_factory=lambda: ["*"])

    dashscope_api_key: str = ""
    dashscope_base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    dashscope_model: str = "qwen-plus"

    auth_token_ttl_hours: int = 24 * 30
    password_hash_iterations: int = 120000
    sms_code_ttl_minutes: int = 10

    wechat_app_id: str = ""
    wechat_app_secret: str = ""

    oss_access_key_id: str = ""
    oss_access_key_secret: str = ""
    oss_endpoint: str = "https://oss-cn-hangzhou.aliyuncs.com"
    oss_bucket_name: str = ""
    oss_public_base_url: str = ""
    oss_upload_prefix: str = "faraway"
    oss_sign_expire_seconds: int = 3600
    local_media_dir: str = "data/uploads"
    local_media_url_prefix: str = "/media"

    max_image_size_mb: int = 10
    max_video_size_mb: int = 300

    model_config = SettingsConfigDict(env_file=ENV_FILE, env_file_encoding="utf-8")

    @property
    def resolved_sqlite_path(self) -> Path:
        path = Path(self.sqlite_path)
        if path.is_absolute():
            return path
        return (BASE_DIR / path).resolve()

    @property
    def resolved_local_media_dir(self) -> Path:
        path = Path(self.local_media_dir)
        if path.is_absolute():
            return path
        return (BASE_DIR / path).resolve()


settings = Settings()
