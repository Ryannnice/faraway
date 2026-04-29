from __future__ import annotations

from typing import Any


def success_response(data: Any, message: str = "ok") -> dict[str, Any]:
    return {"code": 0, "message": message, "data": data}
