from typing import Any

from sqlalchemy.orm import Session

from app.db.models import Startup
from app.services.deep_search_service import deep_search_service
from app.services.feature_service import action_plan, competitor_analysis, marketing_plan, swot_analysis


def startup_context(startup: Startup) -> dict[str, Any]:
    return {
        "name": startup.name,
        "description": startup.description,
        "target_customer": startup.target_customer,
        "target_market": startup.target_market,
        "business_model": startup.business_model,
        "goal": startup.goal,
        "budget": float(startup.budget),
        "currency": startup.currency,
        "time_horizon_days": startup.time_horizon_days,
        "language": startup.language,
        "context_revision": startup.context_revision,
    }


async def run_research(startup: Startup, db: Session) -> dict[str, Any]:
    return await deep_search_service.run(startup, db)


async def run_competitor_analysis(startup: Startup, db: Session) -> dict[str, Any]:
    research = await run_research(startup, db)
    result = competitor_analysis(startup, research)
    result["workflow_status"] = research.get("workflow_status", "fallback")
    result["research_snapshot_id"] = research.get("snapshot_id") or research.get("mock_profile_key")
    return result


async def run_swot(startup: Startup, db: Session) -> dict[str, Any]:
    verified = await run_research(startup, db)
    result = swot_analysis(startup, verified)
    result["workflow_status"] = verified.get("workflow_status", "fallback")
    result["research_snapshot_id"] = verified.get("snapshot_id") or verified.get("mock_profile_key")
    return result


async def run_marketing_plan(startup: Startup, db: Session) -> dict[str, Any]:
    verified = await run_research(startup, db)
    strategy = swot_analysis(startup, verified)
    result = marketing_plan(startup, verified, strategy)
    result["workflow_status"] = verified.get("workflow_status", "fallback")
    result["research_snapshot_id"] = verified.get("snapshot_id") or verified.get("mock_profile_key")
    return result


async def run_ad_action_plan(startup: Startup, db: Session) -> dict[str, Any]:
    plan = await run_marketing_plan(startup, db)
    result = action_plan(startup, plan)
    result["workflow_status"] = plan.get("workflow_status", "fallback")
    result["research_snapshot_id"] = plan.get("research_snapshot_id")
    return result
