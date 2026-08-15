from __future__ import annotations

from typing import Any

from app.db.models import Startup
from app.integrations.mcp_gateway import MCPGateway, mcp_gateway
from app.services.evidence_cleaner import clean_research_payload


DEEP_SEARCH_CONTRACT = {
    "market_overview": "string; cite with market_overview_source_ids or use an explicit unknown statement",
    "market_overview_source_ids": "array of source ids supporting market_overview",
    "target_customer_insights": "array of {text, source_ids, confidence}",
    "competitors": "array of {name, strength, weakness, source_ids}",
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
                "Return only source-backed findings. Do not invent market sizes, growth rates, "
                "competitor counts, prices, conversion rates, or any other numeric value. "
                "If a number is not present in a cited source or cannot be derived from cited "
                "sources with a visible methodology, return value null and number_type unknown. "
                "If sources conflict, preserve the conflict and lower confidence."
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
    def fallback(startup: Startup) -> dict[str, Any]:
        return {
            "market_overview": "Unknown: no approved Deep Search result is available.",
            "target_customer_insights": [],
            "competitors": [],
            "market_trends": [],
            "customer_pain_points": [],
            "opportunities": [],
            "threats": [],
            "sources": [],
            "numeric_claims": [],
            "missing_fields": [
                "verified_market_overview",
                "target_customer_insights",
                "competitor_evidence",
                "market_trends",
                "customer_pain_points",
                "opportunities",
                "threats",
                "market_estimates",
            ],
            "conflicts": [],
            "assumptions": [
                "No approved Deep Search tool is configured, so no external claim is presented.",
                f"The requested target market is {startup.target_market}; this is user-provided context, not research evidence.",
            ],
        }

    async def run(self, startup: Startup) -> dict[str, Any]:
        tool_result = await self.gateway.run(
            "market_research",
            self.build_request(startup),
            self.fallback(startup),
        )
        cleaned = clean_research_payload(tool_result.result)
        cleaned["workflow_status"] = tool_result.status
        cleaned["tool"] = tool_result.tool
        cleaned["tool_error"] = tool_result.error
        cleaned["data_quality"]["gateway_assumptions"] = tool_result.assumptions
        cleaned["data_quality"]["gateway_missing_fields"] = tool_result.missing_fields
        return cleaned


deep_search_service = DeepSearchService(mcp_gateway)
