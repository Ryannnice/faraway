from __future__ import annotations

import re

USERNAME_RE = re.compile(r"^[A-Za-z0-9_]{3,32}$")
WORD_SPLIT_RE = re.compile(r"[\s,，。.!！?？;；:：/\\|()（）【】\[\]<>《》\-_]+")


def normalize_username(username: str) -> str:
    return username.strip().lower()


def normalize_destination(destination: str) -> str:
    collapsed = re.sub(r"\s+", " ", destination.strip())
    return collapsed.lower()


def tokenize_preference_text(text: str) -> set[str]:
    parts = [item.strip().lower() for item in WORD_SPLIT_RE.split(text) if item.strip()]
    return {item for item in parts if item}
