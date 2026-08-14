from typing import Any


class Database:
    """Minimal database placeholder for future persistence wiring."""

    async def connect(self) -> None:
        return None

    async def disconnect(self) -> None:
        return None

    async def ping(self) -> dict[str, Any]:
        return {"status": "ok"}


db = Database()
