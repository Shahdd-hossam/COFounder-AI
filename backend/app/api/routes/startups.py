from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import database_session
from app.core.config import get_settings
from app.db.repositories import get_workflow_run
from app.schemas.startups import StartupCreate, StartupResponse, StartupUpdate, WorkflowRunResponse
from app.services.startup_service import StartupNotFoundError, startup_service

router = APIRouter(prefix="/startups", tags=["Startups"])
workflow_router = APIRouter(prefix="/workflows", tags=["Workflows"])


def owner_id() -> str:
    # Replace with the existing authenticated subject when auth is added.
    return get_settings().demo_owner_id


@router.post("", response_model=StartupResponse, status_code=status.HTTP_201_CREATED)
def create_startup(
    payload: StartupCreate,
    db: Session = Depends(database_session),
) -> StartupResponse:
    return startup_service.create(db, owner_id(), payload)


@router.get("", response_model=list[StartupResponse])
def list_startups(
    db: Session = Depends(database_session),
) -> list[StartupResponse]:
    return startup_service.list(db, owner_id())


@router.get("/{startup_id}", response_model=StartupResponse)
def get_startup(
    startup_id: int,
    db: Session = Depends(database_session),
) -> StartupResponse:
    try:
        return startup_service.get(db, owner_id(), startup_id)
    except StartupNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Startup not found") from exc


@router.patch("/{startup_id}", response_model=StartupResponse)
def update_startup(
    startup_id: int,
    payload: StartupUpdate,
    db: Session = Depends(database_session),
) -> StartupResponse:
    try:
        return startup_service.update(db, owner_id(), startup_id, payload)
    except StartupNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Startup not found") from exc


@workflow_router.get("/{run_id}", response_model=WorkflowRunResponse)
def get_workflow(
    run_id: int,
    db: Session = Depends(database_session),
) -> WorkflowRunResponse:
    run = get_workflow_run(db, run_id, owner_id())
    if run is None:
        raise HTTPException(status_code=404, detail="Workflow run not found")
    return run
