from collections.abc import Generator
from typing import Any

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import Settings

_engine: Engine | None = None
_session_factory: sessionmaker[Session] | None = None


def _engine_kwargs(settings: Settings) -> dict[str, Any]:
    # SQLite does not accept pool_size/max_overflow. The Manus database URL
    # should use the matching SQLAlchemy driver in the deployed environment.
    if settings.database_url.startswith("sqlite"):
        return {"connect_args": {"check_same_thread": False}, "echo": settings.db_echo}
    return {
        "pool_pre_ping": True,
        "pool_recycle": settings.db_pool_recycle,
        "pool_size": settings.db_pool_size,
        "max_overflow": settings.db_max_overflow,
        "echo": settings.db_echo,
    }


def get_engine(settings: Settings) -> Engine:
    global _engine
    if _engine is None:
        if not settings.database_url:
            raise RuntimeError("DATABASE_URL is required for database-backed operations")
        _engine = create_engine(settings.database_url, **_engine_kwargs(settings))
    return _engine


def get_session_factory(settings: Settings) -> sessionmaker[Session]:
    global _session_factory
    if _session_factory is None:
        _session_factory = sessionmaker(
            bind=get_engine(settings),
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )
    return _session_factory


def get_db(settings: Settings) -> Generator[Session, None, None]:
    db = get_session_factory(settings)()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def check_database(settings: Settings) -> bool:
    with get_engine(settings).connect() as connection:
        connection.execute(text("SELECT 1"))
    return True


def reset_engine_for_tests() -> None:
    global _engine, _session_factory
    if _engine is not None:
        _engine.dispose()
    _engine = None
    _session_factory = None
