from __future__ import annotations

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


def import_models() -> None:
    from app.modules.auth import model as _auth_model  # noqa: F401
    from app.modules.matches import model as _match_model  # noqa: F401
    from app.modules.media import model as _media_model  # noqa: F401
    from app.modules.notifications import model as _notice_model  # noqa: F401
    from app.modules.users import model as _user_model  # noqa: F401


import_models()
