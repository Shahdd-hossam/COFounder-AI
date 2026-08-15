from collections.abc import Generator

from app.core.config import get_settings
from app.db.session import get_db


def database_session() -> Generator:
    yield from get_db(get_settings())
