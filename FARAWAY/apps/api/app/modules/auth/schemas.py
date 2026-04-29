from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.text import USERNAME_RE


class RegisterRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    username: str = Field(min_length=3, max_length=32)
    password: str = Field(min_length=6, max_length=128)

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        if not USERNAME_RE.fullmatch(value):
            raise ValueError("username must be 3-32 chars of letters, digits, underscore")
        return value


class PasswordLoginRequest(RegisterRequest):
    pass
