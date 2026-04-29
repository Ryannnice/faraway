from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.constants import Gender


class UserProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    nickname: str
    avatar: str
    bio: str
    gender: str
    created_at: datetime
    updated_at: datetime


class UserSummaryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    nickname: str
    avatar: str


class UpdateProfileRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    nickname: str | None = Field(default=None, min_length=1, max_length=32)
    bio: str | None = Field(default=None, max_length=300)
    avatar: str | None = Field(default=None, max_length=500)
    gender: str | None = None

    @field_validator("nickname")
    @classmethod
    def validate_nickname(cls, value: str | None) -> str | None:
        if value is None:
            return value
        stripped = value.strip()
        if not stripped or len(stripped) > 32:
            raise ValueError("nickname length must be 1-32")
        return stripped

    @field_validator("gender")
    @classmethod
    def validate_gender(cls, value: str | None) -> str | None:
        if value is None:
            return value
        if value not in {item.value for item in Gender}:
            raise ValueError("invalid gender")
        return value
