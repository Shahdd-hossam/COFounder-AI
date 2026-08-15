from __future__ import annotations

from typing import Any

from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.models import Startup
from app.integrations.manus_api_fallback import ManusFallbackError, ManusResearchFallback
from app.integrations.mcp_gateway import MCPGateway, mcp_gateway
from app.services.evidence_cleaner import clean_research_payload
from app.services.estimate_service import add_planning_estimates
from app.services.llm_reasoning_service import LLMReasoningError, llm_reasoning_service
from app.services.mock_research_service import match_profile


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
            "missing_fields": ["verified_market_overview", "target_customer_insights", "competitor_evidence", "market_trends", "customer_pain_points", "opportunities", "threats", "market_estimates"],
            "conflicts": [],
            "assumptions": [
                "Live research was unavailable; no external claim is presented.",
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

    async def _enrich_with_llm(self, startup: Startup, payload: dict[str, Any], errors: list[str]) -> dict[str, Any]:
        settings = get_settings()
        try:
            reasoning = await llm_reasoning_service.enrich(startup, payload, settings)
        except LLMReasoningError as exc:
            errors.append(str(exc))
            return payload
        if not reasoning:
            return payload
        result = dict(payload)
        result["llm_reasoning"] = reasoning.get("reasoning_summary")
        result["llm_estimate_mode"] = "structured_reasoning"
        result["estimated_findings"] = list(result.get("estimated_findings") or [])
        result["estimated_findings"].extend([
            {**item, "number_type": "modeled_estimate", "source_ids": [], "evidence_status": "llm_estimate"}
            for item in reasoning.get("additional_opportunities", []) + reasoning.get("additional_threats", [])
        ])
        result["estimated_numeric_claims"] = list(result.get("estimated_numeric_claims") or [])
        result["estimated_numeric_claims"].extend([
            {**claim, "number_type": "modeled_estimate", "source_ids": [], "geography": startup.target_market, "currency": claim.get("currency"), "unit": claim.get("unit") or "planning units"}
            for claim in reasoning.get("estimated_numeric_claims", [])
        ])
        result["llm_assumptions"] = reasoning.get("assumptions", [])
        result["validation_tasks"] = list(result.get("validation_tasks") or []) + reasoning.get("validation_tasks", [])
        quality = dict(result.get("data_quality") or {})
        quality["llm_reasoning"] = "used"
        result["data_quality"] = quality
        existing_claims = list(result.get("numeric_claims") or [])
        result["numeric_claims"] = existing_claims + result["estimated_numeric_claims"]
        return result

    async def run(self, startup: Startup, db: Session) -> dict[str, Any]:
        gateway_result = await self.gateway.run("market_research", self.build_request(startup), self.fallback(startup))
        errors: list[str] = []
        if gateway_result.error:
            errors.append(f"Primary research error: {gateway_result.error}")
        if gateway_result.status not in {"fallback", "failed"}:
            cleaned = clean_research_payload(gateway_result.result)
            cleaned["workflow_status"] = gateway_result.status
            cleaned["tool"] = gateway_result.tool
            cleaned["tool_error"] = gateway_result.error
            cleaned["data_quality"]["fallback_chain"] = ["Tavily/OpenRouter MCP", "Manus API", "database mock profile", "GPT reasoning"]
            return add_planning_estimates(startup, await self._enrich_with_llm(startup, cleaned, errors))

        errors.append("Primary Tavily/OpenRouter research path did not return a verified result.")
        try:
            manus_result = await ManusResearchFallback(get_settings()).run(self.startup_payload(startup))
            cleaned = clean_research_payload(manus_result)
            cleaned["workflow_status"] = "success"
            cleaned["tool"] = "Manus API structured fallback"
            cleaned["tool_error"] = None
            cleaned["data_quality"]["fallback_chain"] = ["Tavily/OpenRouter MCP", "Manus API", "database mock profile", "GPT reasoning"]
            cleaned = await self._enrich_with_llm(startup, cleaned, errors)
            return add_planning_estimates(startup, cleaned)
        except ManusFallbackError as exc:
            errors.append(f"Manus API fallback unavailable: {exc}")
        except Exception as exc:
            errors.append(f"Manus API fallback failed: {type(exc).__name__}")

        try:
            mock_payload, match = match_profile(db, startup)
            cleaned = clean_research_payload(mock_payload)
            cleaned["workflow_status"] = "mock"
            cleaned["tool"] = "Database mock research profile"
            cleaned["tool_error"] = None
            cleaned["data_quality"]["fallback_chain"] = ["Tavily/OpenRouter MCP", "Manus API", "database mock profile", "GPT reasoning"]
            cleaned["data_quality"]["mock_similarity"] = match
            cleaned = await self._enrich_with_llm(startup, cleaned, errors)
            result = add_planning_estimates(startup, cleaned)
            result["data_quality"]["fallback_errors"] = errors
            return result
        except Exception as exc:
            errors.append(f"Database mock profile failed: {type(exc).__name__}")

        cleaned = clean_research_payload(self.fallback(startup, errors))
        cleaned["workflow_status"] = "fallback"
        cleaned["tool"] = "Planning estimate fallback"
        cleaned["tool_error"] = "; ".join(errors)
        cleaned["data_quality"]["fallback_chain"] = ["Tavily/OpenRouter MCP", "Manus API", "database mock profile", "GPT reasoning", "planning estimate fallback"]
        return add_planning_estimates(startup, cleaned)


deep_search_service = DeepSearchService(mcp_gateway)
