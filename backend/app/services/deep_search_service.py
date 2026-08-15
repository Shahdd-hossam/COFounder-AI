from __future__ import annotations

from typing import Any

from app.core.config import get_settings
from app.db.models import Startup
from app.integrations.manus_api_fallback import ManusFallbackError, ManusResearchFallback
from app.integrations.mcp_gateway import MCPGateway, mcp_gateway
from app.services.evidence_cleaner import clean_research_payload
from app.services.estimate_service import add_planning_estimates


DEEP_SEARCH_CONTRACT = {
    "market_overview": "string; cite with market_overview_source_ids or use an explicit unknown statement",
    "market_overview_source_ids": "array of source ids supporting market_overview",
    "target_customer_insights": "array of {text, source_ids, confidence}",
    "competitors": "array of {name, strength, weakness, source_ids, pricing}",
    "market_trends": "array of {text, source_ids, confidence}",
    "customer_pain_points": "array of {text, source_ids, confidence}",
    "opportunities": "array of {text, source_ids, confidence}",
    "threats": "array of {text, source_ids, confidence}",
    "sources": "array of {id, title, publisher, url, retrieved_on, quality}",
    "numeric_claims": "array of claims; source_reported and derived_from_sources require source_ids",
    "missing_fields": "array of fields that could not be verified",
    "conflicts": "array of source conflicts that require user review",
    "assumptions": "array of explicit assumptions; never hide assumptions in prose",
}


class DeepSearchService:
    def __init__(self, gateway: MCPGateway) -> None:
        self.gateway = gateway

    def build_request(self, startup: Startup) -> dict[str, Any]:
        return {
            "instruction": (
                "Use the startup description and context as the primary research query; do not require or rely on the product name. "
                "Return only source-backed findings. Do not invent market sizes, growth rates, competitor counts, prices, conversion rates, "
                "or any other numeric value. If a number is not present in a cited source or cannot be derived from cited sources with a "
                "visible methodology, return value null and number_type unknown. If sources conflict, preserve the conflict and lower confidence."
            ),
            "output_contract": DEEP_SEARCH_CONTRACT,
            "startup": {
                "name": startup.name,
                "description": startup.description,
                "target_customer": startup.target_customer,
                "target_market": startup.target_market,
                "business_model": startup.business_model,
                "goal": startup.goal,
                "language": startup.language,
                "context_revision": startup.context_revision,
            },
        }

    @staticmethod
    def fallback(startup: Startup, errors: list[str] | None = None) -> dict[str, Any]:
        return {
            "market_overview": "Unknown: no verified research result is available.",
            "market_overview_source_ids": [],
            "target_customer_insights": [],
            "competitors": [],
            "market_trends": [],
            "customer_pain_points": [],
            "opportunities": [],
            "threats": [],
            "sources": [],
            "numeric_claims": [],
            "missing_fields": [
                "verified_market_overview", "target_customer_insights", "competitor_evidence", "market_trends",
                "customer_pain_points", "opportunities", "threats", "market_estimates",
            ],
            "conflicts": [],
            "assumptions": [
                "Tavily/OpenRouter research failed or was unavailable; no external claim is presented.",
                f"The description and target market for {startup.name} are user-provided context, not research evidence.",
                *(errors or []),
            ],
        }

    @staticmethod
    def startup_payload(startup: Startup) -> dict[str, Any]:
        return {
            "name": startup.name,
            "description": startup.description,
            "target_customer": startup.target_customer,
            "target_market": startup.target_market,
            "business_model": startup.business_model,
            "goal": startup.goal,
            "budget": str(startup.budget),
            "currency": startup.currency,
            "time_horizon_days": startup.time_horizon_days,
            "language": startup.language,
            "context_revision": startup.context_revision,
        }

    async def run(self, startup: Startup) -> dict[str, Any]:
        request = self.build_request(startup)
        gateway_result = await self.gateway.run("market_research", request, self.fallback(startup))
        gateway_result_dict = gateway_result.as_dict()
        errors: list[str] = []
        if gateway_result.error:
            errors.append(f"Primary research error: {gateway_result.error}")
        if gateway_result.status in {"fallback", "failed"}:
            errors.append("Primary Tavily/MCP research path did not return a verified result.")
            try:
                manus_result = await ManusResearchFallback(get_settings()).run(self.startup_payload(startup))
                cleaned = clean_research_payload(manus_result)
                cleaned["workflow_status"] = "success"
                cleaned["tool"] = "Manus API structured fallback"
                cleaned["tool_error"] = None
                cleaned["data_quality"]["fallback_chain"] = ["Tavily/OpenRouter MCP", "Manus API"]
                cleaned["data_quality"]["primary_path_status"] = gateway_result.status
                cleaned["data_quality"]["gateway_assumptions"] = gateway_result.assumptions
                return add_planning_estimates(startup, cleaned)
            except ManusFallbackError as exc:
                errors.append(f"Manus API fallback unavailable: {exc}")
            except Exception as exc:
                errors.append(f"Manus API fallback failed: {type(exc).__name__}")

        cleaned = clean_research_payload(gateway_result.result)
        cleaned["workflow_status"] = gateway_result.status
        cleaned["tool"] = gateway_result.tool
        cleaned["tool_error"] = gateway_result.error
        cleaned["data_quality"]["gateway_assumptions"] = gateway_result.assumptions
        cleaned["data_quality"]["gateway_missing_fields"] = gateway_result.missing_fields
        cleaned["data_quality"]["fallback_chain"] = ["Tavily/OpenRouter MCP", "Manus API"]
        if errors:
            cleaned["data_quality"]["fallback_errors"] = errors
        return add_planning_estimates(startup, cleaned)


deep_search_service = DeepSearchService(mcp_gateway)
