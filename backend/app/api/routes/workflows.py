from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import database_session
from app.core.config import get_settings
from app.db.repositories import create_workflow_run
from app.db.models import WorkflowRun
from app.services.startup_service import StartupNotFoundError, startup_service
from app.services.workflow_service import run_ad_action_plan, run_competitor_analysis, run_marketing_plan, run_research, run_swot

router = APIRouter(prefix="/startups", tags=["Workflows"])


def owner_id() -> str:
    return get_settings().demo_owner_id


def mark_run(run: WorkflowRun, status: str, result: dict | None = None, error: Exception | None = None) -> None:
    run.status = status
    run.progress_percent = 100 if status in {"ready", "partial", "failed"} else run.progress_percent
    run.stage = "completed" if status in {"ready", "partial"} else "failed" if status == "failed" else run.stage
    run.result_json = result
    run.error_message = str(error) if error else None
    run.completed_at = datetime.now(timezone.utc) if status in {"ready", "partial", "failed"} else None


async def execute_workflow(startup_id: int, feature: str, fn, db: Session):
    try:
        startup = startup_service.get(db, owner_id(), startup_id)
    except StartupNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Startup not found") from exc

    run = create_workflow_run(db, startup, feature)
    run.status = "running"
    run.stage = "generating"
    run.progress_percent = 20
    db.flush()
    try:
        result = await fn(startup, db)
        tool_status = result.get("workflow_status", result.get("status"))
        mark_run(run, "partial" if tool_status in {"fallback", "failed"} else "ready", result)
    except Exception as exc:
        mark_run(run, "failed", error=exc)
    db.flush()
    return run


@router.post("/{startup_id}/market-research/runs")
async def research_run(startup_id: int, db: Session = Depends(database_session)):
    return await execute_workflow(startup_id, "market_research", run_research, db)


@router.post("/{startup_id}/competitor-analysis/runs")
async def competitor_run(startup_id: int, db: Session = Depends(database_session)):
    return await execute_workflow(startup_id, "competitor_analysis", run_competitor_analysis, db)


@router.post("/{startup_id}/swot/runs")
async def swot_run(startup_id: int, db: Session = Depends(database_session)):
    return await execute_workflow(startup_id, "swot", run_swot, db)


@router.post("/{startup_id}/marketing-plan/runs")
async def marketing_run(startup_id: int, db: Session = Depends(database_session)):
    return await execute_workflow(startup_id, "marketing_plan", run_marketing_plan, db)


@router.post("/{startup_id}/action-plans/runs")
async def action_plan_run(startup_id: int, db: Session = Depends(database_session)):
    return await execute_workflow(startup_id, "ad_action_plan", run_ad_action_plan, db)
