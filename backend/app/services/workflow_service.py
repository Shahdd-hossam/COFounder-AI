from typing import Any

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


async def run_research(startup: Startup) -> dict[str, Any]:
    return await deep_search_service.run(startup)


async def run_competitor_analysis(startup: Startup) -> dict[str, Any]:
    research = await run_research(startup)
    result = competitor_analysis(startup, research)
    result["workflow_status"] = research.get("workflow_status", "fallback")
    result["research_snapshot_id"] = research.get("snapshot_id")
    return result


async def run_swot(startup: Startup, research: dict[str, Any] | None = None) -> dict[str, Any]:
    verified = research or await run_research(startup)
    result = swot_analysis(startup, verified)
    result["workflow_status"] = verified.get("workflow_status", "fallback")
    result["research_snapshot_id"] = verified.get("snapshot_id")
    return result


async def run_marketing_plan(startup: Startup, research: dict[str, Any] | None = None, swot: dict[str, Any] | None = None) -> dict[str, Any]:
    verified = research or await run_research(startup)
    strategy = swot or swot_analysis(startup, verified)
    result = marketing_plan(startup, verified, strategy)
    result["workflow_status"] = verified.get("workflow_status", "fallback")
    result["research_snapshot_id"] = verified.get("snapshot_id")
    return result


async def run_ad_action_plan(startup: Startup, marketing_plan: dict[str, Any] | None = None) -> dict[str, Any]:
    plan = marketing_plan or await run_marketing_plan(startup)
    result = action_plan(startup, plan)
    result["workflow_status"] = plan.get("workflow_status", "fallback")
    result["research_snapshot_id"] = plan.get("research_snapshot_id")
    return result
