from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


def _normalize_tags(tags: list[str]) -> list[str]:
    normalized: list[str] = []
    seen: set[str] = set()
    for item in tags:
        text = str(item).strip()
        if not text:
            continue
        if len(text) > 12:
            raise ValueError("tag is too long")
        if text in seen:
            continue
        seen.add(text)
        normalized.append(text)
    if len(normalized) > 5:
        raise ValueError("too many tags")
    return normalized


def _normalize_lines(items: list[str], *, field_name: str) -> list[str]:
    normalized: list[str] = []
    for item in items:
        text = str(item).strip()
        if not text:
            continue
        if len(text) > 200:
            raise ValueError(f"{field_name} item is too long")
        normalized.append(text)
    return normalized


class PublishDailyPlan(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    day: int = Field(ge=1)
    activities: list[str]
    food: list[str]
    accommodation: str = Field(min_length=1, max_length=200)

    @field_validator("activities")
    @classmethod
    def validate_activities(cls, value: list[str]) -> list[str]:
        normalized = _normalize_lines(value, field_name="activities")
        if not normalized:
            raise ValueError("activities is required")
        return normalized

    @field_validator("food")
    @classmethod
    def validate_food(cls, value: list[str]) -> list[str]:
        normalized = _normalize_lines(value, field_name="food")
        if not normalized:
            raise ValueError("food is required")
        return normalized


class PublishStrategyRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(min_length=1, max_length=60)
    tags: list[str] = Field(default_factory=list)
    cover_asset_id: str | None = None
    destination: str = Field(min_length=1, max_length=100)
    days: int = Field(ge=1, le=14)
    overview: str = Field(min_length=1, max_length=1000)
    daily_plans: list[PublishDailyPlan]
    tips: list[str] = Field(default_factory=list)

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, value: list[str]) -> list[str]:
        return _normalize_tags(value)

    @field_validator("tips")
    @classmethod
    def validate_tips(cls, value: list[str]) -> list[str]:
        normalized = _normalize_lines(value, field_name="tips")
        if len(normalized) > 10:
            raise ValueError("too many tips")
        return normalized

    @field_validator("cover_asset_id")
    @classmethod
    def normalize_cover_asset_id(cls, value: str | None) -> str | None:
        if value is None:
            return None
        stripped = value.strip()
        return stripped or None

    @model_validator(mode="after")
    def validate_daily_plans(self) -> "PublishStrategyRequest":
        if len(self.daily_plans) != self.days:
            raise ValueError("daily_plans length mismatch")
        return self


class PublishVlogRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(min_length=1, max_length=60)
    content: str = Field(min_length=1, max_length=5000)
    tags: list[str] = Field(default_factory=list)
    image_asset_ids: list[str] = Field(default_factory=list)

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, value: list[str]) -> list[str]:
        return _normalize_tags(value)

    @field_validator("image_asset_ids")
    @classmethod
    def validate_image_asset_ids(cls, value: list[str]) -> list[str]:
        normalized: list[str] = []
        seen: set[str] = set()
        for item in value:
            text = str(item).strip()
            if not text or text in seen:
                continue
            seen.add(text)
            normalized.append(text)
        if len(normalized) > 9:
            raise ValueError("too many images")
        return normalized
