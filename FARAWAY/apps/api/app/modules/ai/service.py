from __future__ import annotations

import json
import logging
from typing import Any

import httpx
from fastapi import HTTPException, status

from app.core.config import settings
from app.modules.ai.schemas import DailyPlan, GenerateStrategyRequest, GeneratedStrategy

logger = logging.getLogger(__name__)


def _local_strategy(req: GenerateStrategyRequest) -> dict[str, Any]:
    return {
        "destination": req.destination,
        "overview": f"这是一份为{req.destination}准备的 {req.days} 天轻量旅行攻略。",
        "daily_plans": [
            {
                "day": day,
                "activities": [f"第 {day} 天目的地核心片区探索", "预留机动时间拍照和休息"],
                "food": ["当地热门餐厅", "便利补给点"],
                "accommodation": req.hotel_requirement or "交通便利区域住宿",
            }
            for day in range(1, req.days + 1)
        ],
        "tips": ["提前确认天气和预约信息", "重要证件与药物随身携带"],
    }


def _extract_json_payload(content: str) -> Any:
    text = content.strip()
    if text.startswith("```"):
        text = text.strip("`")
        text = text.removeprefix("json").strip()
    return json.loads(text)


def _normalize_strategy(raw: Any, req: GenerateStrategyRequest) -> GeneratedStrategy:
    if not isinstance(raw, dict):
        raise ValueError("strategy payload is not an object")

    daily_plans = raw.get("daily_plans", raw.get("dailyPlans"))
    if not isinstance(daily_plans, list) or len(daily_plans) != req.days:
        raise ValueError("daily_plans length mismatch")

    normalized_days: list[DailyPlan] = []
    for index, item in enumerate(daily_plans, start=1):
        if not isinstance(item, dict):
            raise ValueError("daily plan item must be object")
        try:
            normalized_days.append(
                DailyPlan(
                    day=int(item.get("day", index)),
                    activities=[str(part) for part in item["activities"]],
                    food=[str(part) for part in item["food"]],
                    accommodation=str(item["accommodation"]),
                )
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError("daily plan item invalid") from exc

    return GeneratedStrategy(
        destination=str(raw.get("destination", req.destination)),
        overview=str(raw.get("overview", "")),
        daily_plans=normalized_days,
        tips=[str(item) for item in raw.get("tips", [])],
    )


def generate_strategy(req: GenerateStrategyRequest) -> dict:
    if not settings.dashscope_api_key:
        return _normalize_strategy(_local_strategy(req), req).model_dump()

    prompt = {
        "destination": req.destination,
        "days": req.days,
        "budget": req.budget,
        "hotel_requirement": req.hotel_requirement,
        "allergies": req.allergies,
        "pace": req.pace,
        "group_type": req.group_type,
    }
    try:
        response = httpx.post(
            f"{settings.dashscope_base_url.rstrip('/')}/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.dashscope_api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": settings.dashscope_model,
                "messages": [
                    {"role": "system", "content": "你是旅行规划助手，只返回严格 JSON。"},
                    {"role": "user", "content": json.dumps(prompt, ensure_ascii=False)},
                ],
                "response_format": {"type": "json_object"},
            },
            timeout=settings.strategy_ai_timeout_seconds,
        )
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        raw = _extract_json_payload(content)
        return _normalize_strategy(raw, req).model_dump()
    except (httpx.HTTPError, KeyError, ValueError, json.JSONDecodeError) as exc:
        logger.exception("strategy generation failed destination=%s", req.destination)
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="strategy generation failed") from exc


def generate_meeting_place(destination: str, preference_tags: list[str], preference_text: str) -> str:
    fallback = f"{destination} 主城区地标广场 / 游客中心附近"
    if not settings.dashscope_api_key:
        return fallback

    prompt = (
        "请给出一个适合第一次见面的白天公共地点，要求交通方便、人流较多、容易辨认。"
        f"目的地：{destination}；标签：{'、'.join(preference_tags) or '无'}；补充：{preference_text or '无'}。"
        "只返回一句中文地点文本。"
    )
    try:
        response = httpx.post(
            f"{settings.dashscope_base_url.rstrip('/')}/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.dashscope_api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": settings.dashscope_model,
                "messages": [
                    {"role": "system", "content": "你是旅行安全助手，回答必须可直接展示。"},
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.2,
            },
            timeout=settings.meeting_place_ai_timeout_seconds,
        )
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"].strip()
        return content.splitlines()[0].strip() or fallback
    except Exception:
        logger.warning("meeting place generation fallback destination=%s", destination)
        return fallback
