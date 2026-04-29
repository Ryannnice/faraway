from __future__ import annotations

from pydantic import BaseModel


class UploadImageResponse(BaseModel):
    asset_id: str
    url: str
