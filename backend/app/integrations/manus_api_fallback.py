from __future__ import annotations

import asyncio
from typing import Any

import httpx

from app.core.config import Settings


class ManusFallbackError(RuntimeError):
    pass


RESEARCH_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "market_overview": {"type": "string"},
        "market_overview_source_ids": {"type": "array", "items": {"type": "string"}},
        "target_customer_insights": {"type": "array", "items": {"$ref": "#/$defs/finding"}},
        "market_trends": {"type": "array", "items": {"$ref": "#/$defs/finding"}},
        "customer_pain_points": {"type": "array", "items": {"$ref": "#/$defs/finding"}},
        "competitors": {"type": "array", "items": {"$ref": "#/$defs/competitor"}},
        "opportunities": {"type": "array", "items": {"$ref": "#/$defs/finding"}},
        "threats": {"type": "array", "items": {"$ref": "#/$defs/finding"}},
        "sources": {"type": "array", "items": {"$ref": "#/$defs/source"}},
        "numeric_claims": {"type": "array", "items": {"$ref": "#/$defs/claim"}},
        "estimated_findings": {"type": "array", "items": {"$ref": "#/$defs/estimate_finding"}},
        "estimated_numeric_claims": {"type": "array", "items": {"$ref": "#/$defs/claim"}},
        "missing_fields": {"type": "array", "items": {"type": "string"}},
        "conflicts": {"type": "array", "items": {"type": "string"}},
        "assumptions": {"type": "array", "items": {"type": "string"}},
    },
    "required": [
        "market_overview", "market_overview_source_ids", "target_customer_insights", "market_trends",
        "customer_pain_points", "competitors", "opportunities", "threats",         "sources", "numeric_claims", "estimated_findings", "estimated_numeric_claims",
        "missing_fields", "conflicts", "assumptions",

    ],
    "additionalProperties": False,
    "$defs": {
        "finding": {
            "type": "object",
            "properties": {
                "text": {"type": "string"},
                "source_ids": {"type": "array", "items": {"type": "string"}},
                "confidence": {"type": "string", "enum": ["low", "medium", "high"]},
            },
            "required": ["text", "source_ids", "confidence"],
            "additionalProperties": False,
        },
        "competitor": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "strength": {"type": "string"},
                "weakness": {"type": "string"},
                "source_ids": {"type": "array", "items": {"type": "string"}},
                "pricing": {"type": "string"},
            },
            "required": ["name", "strength", "weakness", "source_ids", "pricing"],
            "additionalProperties": False,
        },
        "source": {
            "type": "object",
            "properties": {
                "id": {"type": "string"},
                "title": {"type": "string"},
                "publisher": {"type": "string"},
                "url": {"type": "string"},
                "retrieved_on": {"type": "string"},
                "quality": {"type": "string", "enum": ["low", "medium", "high"]},
            },
            "required": ["id", "title", "publisher", "url", "retrieved_on", "quality"],
            "additionalProperties": False,
        },
        "estimate_finding": {
            "type": "object",
            "properties": {
                "text": {"type": "string"},
                "category": {"type": "string"},
                "number_type": {"type": "string", "enum": ["modeled_estimate", "unknown"]},
                "confidence": {"type": "string", "enum": ["low", "medium", "high"]},
                "methodology": {"type": "string"},
                "assumptions": {"type": "array", "items": {"type": "string"}},
                "validation_plan": {"type": "string"},
            },
            "required": ["text", "category", "number_type", "confidence", "methodology", "assumptions", "validation_plan"],
            "additionalProperties": False,
        },
        "claim": {
            "type": "object",
            "properties": {
                "label": {"type": "string"},
                "value": {"type": ["string", "null"]},
                "unit": {"type": "string"},
                "currency": {"type": ["string", "null"]},
                "geography": {"type": "string"},
                "period": {"type": "string"},
                "number_type": {"type": "string", "enum": ["source_reported", "derived_from_sources", "modeled_estimate", "unknown"]},
                "source_ids": {"type": "array", "items": {"type": "string"}},
                "methodology": {"type": ["string", "null"]},
                "confidence": {"type": "string", "enum": ["low", "medium", "high"]},
                "assumptions": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["label", "value", "unit", "currency", "geography", "period", "number_type", "source_ids", "methodology", "confidence", "assumptions"],
            "additionalProperties": False,
        },
    },
}


def _extract_task_id(payload: dict[str, Any]) -> str | None:
    for candidate in (payload.get("task_id"), payload.get("id"), (payload.get("task") or {}).get("task_id"), (payload.get("task") or {}).get("id")):
        if candidate:
            return str(candidate)
    return None


class ManusResearchFallback:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def _headers(self) -> dict[str, str]:
        return {"x-manus-api-key": self.settings.manus_api_key or "", "Content-Type": "application/json"}

    def _prompt(self, startup: dict[str, Any]) -> str:
        return (
            "Perform source-backed market research for the following startup context. Use the description, target customer, "
            "market, business model, language, and goal; do not use the product name as the primary search key. "
            "Find market context, customer pain points, direct and indirect competitors, trends, opportunities, and threats. "
            "Every factual finding must include source_ids linked to a valid URL. Every numeric claim must be explicitly reported "
            "by a source or visibly derived from cited sources. Never invent TAM, SAM, SOM, prices, CAC, conversion rates, users, "
            "growth rates, or competitor counts. If evidence is missing, return an empty array or an explicit unknown and add a missing_fields entry. "
            "Also provide planning estimates for fields that need a decision, such as interview targets, pilot cohort size, budget allocation, or experiment targets. "
            "Every estimate must use number_type modeled_estimate, include methodology, assumptions, confidence, and a validation_plan, and must never be described as observed market data.\n\n"
            f"Startup context: {startup}"
        )

    async def run(self, startup: dict[str, Any]) -> dict[str, Any]:
        if not self.settings.manus_enabled:
            raise ManusFallbackError("Manus API fallback is disabled")
        if not self.settings.manus_api_key:
            raise ManusFallbackError("MANUS_API_KEY is not configured")

        async with httpx.AsyncClient(base_url=self.settings.manus_api_base_url, headers=self._headers(), timeout=self.settings.manus_timeout_seconds) as client:
            create_response = await client.post(
                "/v2/task.create",
                json={"message": {"content": self._prompt(startup)}, "structured_output_schema": RESEARCH_SCHEMA},
            )
            create_response.raise_for_status()
            created = create_response.json()
            task_id = _extract_task_id(created)
            if not task_id:
                raise ManusFallbackError("Manus API did not return a task id")

            deadline = asyncio.get_running_loop().time() + self.settings.manus_timeout_seconds
            while asyncio.get_running_loop().time() < deadline:
                messages_response = await client.get("/v2/task.listMessages", params={"task_id": task_id, "order": "asc"})
                messages_response.raise_for_status()
                payload = messages_response.json()
                messages = payload.get("messages", payload.get("data", [])) if isinstance(payload, dict) else []
                for event in messages if isinstance(messages, list) else []:
                    if event.get("type") == "structured_output_result":
                        result = event.get("structured_output_result", {})
                        if not result.get("success"):
                            raise ManusFallbackError(result.get("error") or "Manus structured output failed")
                        value = result.get("value")
                        if not isinstance(value, dict):
                            raise ManusFallbackError("Manus structured output was not an object")
                        return value
                    if event.get("type") == "status_update" and event.get("status") == "error":
                        raise ManusFallbackError(str(event))
                await asyncio.sleep(self.settings.manus_poll_interval_seconds)

        raise ManusFallbackError("Manus API fallback timed out")
