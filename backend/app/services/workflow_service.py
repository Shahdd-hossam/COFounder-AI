from typing import Any

from app.db.models import Startup
from app.integrations.mcp_gateway import mcp_gateway


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


def research_fallback(startup: Startup) -> dict[str, Any]:
    return {
        "market_overview": "Insufficient verified research: connect an approved Deep Search tool.",
        "target_customer_insights": [],
        "competitors": [],
        "market_trends": [],
        "customer_pain_points": [],
        "opportunities": [],
        "threats": [],
        "numeric_claims": [],
        "sources": [],
    }


def swot_fallback(startup: Startup, research: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "strengths": [{"text": f"Clear focus on {startup.target_customer}.", "basis": "startup_context"}],
        "weaknesses": [{"text": "Verified market evidence is not yet connected.", "basis": "missing_research"}],
        "opportunities": [{"text": f"Test demand in {startup.target_market}.", "basis": "startup_context"}],
        "threats": [{"text": "Competitor and channel pressure remain unverified.", "basis": "missing_research"}],
    }


def marketing_fallback(startup: Startup, research: dict[str, Any] | None = None, swot: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "objective": {
            "title": startup.goal,
            "description": "Generate a validated plan after research and strategy tools are connected.",
            "target": startup.goal,
            "deadline": f"{startup.time_horizon_days} days",
        },
        "personas": [{"name": startup.target_customer, "description": "Context-derived persona; validate with research.", "pain_points": [], "motivations": [], "preferred_channels": []}],
        "channels": [],
        "campaigns": [],
        "content_calendar": [],
        "budget_allocation": [],
        "kpis": [],
        "action_items": [],
        "data_quality": {"confidence": "low", "assumptions": ["Marketing MCP/LLM is not configured."]},
    }


def ads_fallback(startup: Startup, marketing_plan: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "campaigns": [],
        "tasks": [{"stable_key": "connect_ads_tool", "task": "Connect an approved advertising planning tool before creating execution-ready ad recommendations.", "status": "todo"}],
        "execution_enabled": False,
    }


async def run_research(startup: Startup) -> dict[str, Any]:
    result = await mcp_gateway.run("market_research", startup_context(startup), research_fallback(startup))
    return result.as_dict()


async def run_swot(startup: Startup, research: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = {"startup": startup_context(startup), "research": research or {}}
    result = await mcp_gateway.run("swot", payload, swot_fallback(startup, research))
    return result.as_dict()


async def run_marketing_plan(startup: Startup, research: dict[str, Any] | None = None, swot: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = {"startup": startup_context(startup), "research": research or {}, "swot": swot or {}}
    result = await mcp_gateway.run("marketing_plan", payload, marketing_fallback(startup, research, swot))
    return result.as_dict()


async def run_ad_action_plan(startup: Startup, marketing_plan: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = {"startup": startup_context(startup), "marketing_plan": marketing_plan or {}}
    result = await mcp_gateway.run("ad_action_plan", payload, ads_fallback(startup, marketing_plan))
    return result.as_dict()
