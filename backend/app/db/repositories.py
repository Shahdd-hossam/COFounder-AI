from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Startup, WorkflowRun
from app.schemas.startups import StartupCreate, StartupUpdate


def create_startup(db: Session, owner_id: str, payload: StartupCreate) -> Startup:
    startup = Startup(owner_id=owner_id, context_revision=1, **payload.model_dump())
    db.add(startup)
    db.flush()
    return startup


def list_startups(db: Session, owner_id: str) -> list[Startup]:
    return list(
        db.scalars(
            select(Startup).where(Startup.owner_id == owner_id).order_by(Startup.updated_at.desc())
        )
    )


def get_startup(db: Session, startup_id: int, owner_id: str) -> Startup | None:
    return db.scalar(
        select(Startup).where(Startup.id == startup_id, Startup.owner_id == owner_id)
    )


def update_startup(
    db: Session, startup: Startup, payload: StartupUpdate
) -> Startup:
    changes = payload.model_dump()
    context_changed = any(getattr(startup, key) != value for key, value in changes.items())
    for key, value in changes.items():
        setattr(startup, key, value)
    if context_changed:
        startup.context_revision += 1
    db.add(startup)
    db.flush()
    return startup


def create_workflow_run(
    db: Session,
    startup: Startup,
    feature: str,
    tool_name: str | None = None,
    input_revisions: dict | None = None,
) -> WorkflowRun:
    run = WorkflowRun(
        startup_id=startup.id,
        feature=feature,
        status="queued",
        progress_percent=0,
        tool_name=tool_name,
        context_revision=startup.context_revision,
        input_revisions_json=input_revisions or {},
    )
    db.add(run)
    db.flush()
    return run


def get_workflow_run(db: Session, run_id: int, owner_id: str) -> WorkflowRun | None:
    return db.scalar(
        select(WorkflowRun)
        .join(Startup, WorkflowRun.startup_id == Startup.id)
        .where(WorkflowRun.id == run_id, Startup.owner_id == owner_id)
    )
