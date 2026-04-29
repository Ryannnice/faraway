from __future__ import annotations

from collections.abc import Generator
from contextlib import contextmanager

from sqlalchemy.orm import Session


@contextmanager
def managed_transaction(session: Session) -> Generator[None, None, None]:
    if session.in_transaction():
        with session.begin_nested():
            yield
        return

    with session.begin():
        yield
