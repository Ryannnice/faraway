from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.constants import PREFERENCE_TAGS


class CreateRealtimeMatchRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    destination: str = Field(min_length=1, max_length=100)
    travel_start_date: date
    travel_end_date: date
    preference_tags: list[str] = Field(default_factory=list)
    preference_text: str = Field(default="", max_length=500)

    @field_validator("preference_tags")
    @classmethod
    def validate_tags(cls, value: list[str]) -> list[str]:
        deduped: list[str] = []
        seen: set[str] = set()
        for item in value:
            if item not in PREFERENCE_TAGS:
                raise ValueError("invalid preference tag")
            if item not in seen:
                seen.add(item)
                deduped.append(item)
        return deduped


class SubmitRemarkRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    remark: str = Field(min_length=1, max_length=200)


class CandidateView(BaseModel):
    candidate_id: str
    peer_user_id: str
    peer_nickname: str
    peer_avatar: str
    meeting_place_text: str
    match_summary: str
    decision_expires_at: datetime
    my_decision: str
    peer_decision: str


class PairView(BaseModel):
    pair_id: str
    status: str
    peer_user_id: str
    peer_nickname: str
    peer_avatar: str
    meet_time: datetime
    meet_location_text: str
    my_remark: str
    peer_remark: str
