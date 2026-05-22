"""SQLAlchemy engine + session factory.

The Postgres password is passed through ``URL.create`` so it is never interpolated
into a string the way ``CONNECTION_STRING_PSQL`` used to do. ``echo`` is gated by
``SQL_ECHO`` (default off) so we don't dump bound parameters to stdout in prod.
"""

from __future__ import annotations

from collections.abc import Generator
from contextlib import contextmanager

import structlog
from sqlalchemy import URL, Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from nightsservice.settings import get_app_settings, get_db_settings

logger = structlog.get_logger(__name__)


def _build_url(is_local: bool) -> URL | str:
    if is_local:
        return "sqlite:///src/database/nightsretrieval.db"

    db = get_db_settings()
    return URL.create(
        drivername="postgresql+psycopg",
        username=db.DB_USERNAME,
        password=db.DB_PASSWORD,
        host=db.DB_HOST,
        port=db.DB_PORT,
        database=db.DB_DATABASE_NAME,
    )


def init_engine(is_local: bool = False) -> Engine:
    settings = get_app_settings()
    url = _build_url(is_local)
    try:
        return create_engine(url, echo=settings.SQL_ECHO, pool_pre_ping=True, future=True)
    except Exception:
        logger.exception("database_engine_init_failed")
        raise


_session_factory: sessionmaker[Session] | None = None


def get_session_factory(engine: Engine | None = None) -> sessionmaker[Session]:
    global _session_factory
    if _session_factory is None:
        _session_factory = sessionmaker(
            bind=engine or init_engine(),
            expire_on_commit=False,
            future=True,
        )
    return _session_factory


@contextmanager
def session_scope(engine: Engine | None = None) -> Generator[Session]:
    """Provide a transactional scope around a series of operations."""
    factory = get_session_factory(engine)
    session = factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
