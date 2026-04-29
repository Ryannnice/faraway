from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator


class GenerateStrategyRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    destination: str = Field(min_length=1, max_length=100)
    days: int = Field(default=3, ge=1, le=14)
    budget: str = Field(default="", max_length=100)
    hotel_requirement: str = Field(default="", max_length=100)
    allergies: str = Field(default="", max_length=100)
    pace: str = Field(default="", max_length=100)
    group_type: str = Field(default="", max_length=100)

    @field_validator("destination")
    @classmethod
    def validate_destination(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("destination is required")
        return stripped


class DailyPlan(BaseModel):
    day: int
    activities: list[str]
    food: list[str]
    accommodation: str


class GeneratedStrategy(BaseModel):
    destination: str
    overview: str
    daily_plans: list[DailyPlan]
    tips: list[str]
