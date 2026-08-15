from sqlalchemy.orm import Session

from app.db import repositories
from app.schemas.startups import StartupCreate, StartupUpdate


class StartupNotFoundError(Exception):
    pass


class StartupService:
    def create(self, db: Session, owner_id: str, payload: StartupCreate):
        return repositories.create_startup(db, owner_id, payload)

    def list(self, db: Session, owner_id: str):
        return repositories.list_startups(db, owner_id)

    def get(self, db: Session, owner_id: str, startup_id: int):
        startup = repositories.get_startup(db, startup_id, owner_id)
        if startup is None:
            raise StartupNotFoundError
        return startup

    def update(self, db: Session, owner_id: str, startup_id: int, payload: StartupUpdate):
        startup = self.get(db, owner_id, startup_id)
        return repositories.update_startup(db, startup, payload)


startup_service = StartupService()
