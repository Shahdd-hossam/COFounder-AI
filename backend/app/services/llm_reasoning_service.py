from __future__ import annotations

import json
import os
from typing import Any

import httpx

from app.core.config import Settings
from app.db.models import Startup


class LLMReasoningError(RuntimeError):
    pass


REASONING_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "reasoning_summary": {"type": "string"},
        "additional_competitors": {"type": "array", "items": {"type": "object", "properties": {"name": {"type": "string"}, "reason": {"type": "string"}, "strength": {"type": "string"}, "weakness": {"type": "string"}, "pricing": {"type": "string"}}, "required": ["name", "reason", "strength", "weakness", "pricing"], "additionalProperties": False}},
        "additional_opportunities": {"type": "array", "items": {"type": "object", "properties": {"text": {"type": "string"}, "reason": {"type": "string"}, "confidence": {"type": "string", "enum": ["low", "medium", "high"]}}, "required": ["text", "reason", "confidence"], "additionalProperties": False}},
        "additional_threats": {"type": "array", "items": {"type": "object", "properties": {"text": {"type": "string"}, "reason": {"type": "string"}, "confidence": {"type": "string", "enum": ["low", "medium", "high"]}}, "required": ["text", "reason", "confidence"], "additionalProperties": False}},
        "estimated_numeric_claims": {"type": "array", "items": {"type": "object", "properties": {"label": {"type": "string"}, "value": {"type": "string"}, "unit": {"type": "string"}, "currency": {"type": "string"}, "period": {"type": "string"}, "methodology": {"type": "string"}, "confidence": {"type": "string", "enum": ["low", "medium", "high"]}, "assumptions": {"type": "array", "items": {"type": "string"}}, "validation_plan": {"type": "string"}}, "required": ["label", "value", "unit", "currency", "period", "methodology", "confidence", "assumptions", "validation_plan"], "additionalProperties": False}},
        "assumptions": {"type": "array", "items": {"type": "string"}},
        "validation_tasks": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["reasoning_summary", "additional_competitors", "additional_opportunities", "additional_threats", "estimated_numeric_claims", "assumptions", "validation_tasks"],
    "additionalProperties": False,
    "$defs": {
        "competitor": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "reason": {"type": "string"},
                "strength": {"type": "string"},
                "weakness": {"type": "string"},
                "pricing": {"type": "string"},
            },
            "required": ["name", "reason", "strength", "weakness", "pricing"],
            "additionalProperties": False,
        },
        "insight": {
            "type": "object",
            "properties": {
                "text": {"type": "string"},
                "reason": {"type": "string"},
                "confidence": {"type": "string", "enum": ["low", "medium", "high"]},
            },
            "required": ["text", "reason", "confidence"],
            "additionalProperties": False,
        },
        "claim": {
            "type": "object",
            "properties": {
                "label": {"type": "string"},
                "value": {"type": "string"},
                "unit": {"type": "string"},
                "currency": {"type": "string"},
                "period": {"type": "string"},
                "methodology": {"type": "string"},
                "confidence": {"type": "string", "enum": ["low", "medium", "high"]},
                "assumptions": {"type": "array", "items": {"type": "string"}},
                "validation_plan": {"type": "string"},
            },
            "required": ["label", "value", "unit", "currency", "period", "methodology", "confidence", "assumptions", "validation_plan"],
            "additionalProperties": False,
        },
    },
}


def _startup_context(startup: Startup) -> dict[str, Any]:
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
    }


def _config(settings: Settings) -> tuple[str | None, str | None]:
    return (
        settings.llm_api_key or os.getenv("OPENAI_API_KEY"),
        settings.llm_base_url or os.getenv("OPENAI_API_BASE"),
    )


class LLMReasoningService:
    async def enrich(self, startup: Startup, research: dict[str, Any], settings: Settings) -> dict[str, Any] | None:
        if not settings.llm_enabled:
            return None
        api_key, base_url = _config(settings)
        if not api_key or not base_url:
            return None
        payload = {
            "model": settings.llm_model,
            "messages": [
                {"role": "system", "content": "You are a rigorous startup strategy analyst. Reason over the startup context and the research baseline. Do not invent verified facts. If a competitor, numeric value, price, market size, CAC, conversion rate, or demand value is not directly supported by a source in the input, return it only as an explicitly labeled model estimate with assumptions, methodology, confidence, and validation plan. Prefer coherent, useful hypotheses over empty arrays, but never call a hypothesis source-backed."},
                {"role": "user", "content": json.dumps({"startup": _startup_context(startup), "research_baseline": research}, ensure_ascii=False)},
            ],
            "max_completion_tokens": 5000,
            "response_format": {"type": "json_schema", "json_schema": {"name": "strategy_reasoning", "strict": True, "schema": REASONING_SCHEMA}},
        }
        try:
            async with httpx.AsyncClient(base_url=base_url.rstrip("/"), timeout=settings.llm_timeout_seconds, headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}) as client:
                response = await client.post("/chat/completions", json=payload)
                response.raise_for_status()
                body = response.json()
                if "choices" not in body:
                    raise LLMReasoningError(f"LLM response missing choices: {json.dumps(body)[:500]}")
                content = body["choices"][0]["message"]["content"]
                value = json.loads(content)
                if not isinstance(value, dict):
                    raise LLMReasoningError("LLM response was not an object")
                return value
        except httpx.HTTPStatusError as exc:
            detail = exc.response.text[:500].replace(api_key or "", "[redacted]")
            raise LLMReasoningError(f"LLM reasoning failed: HTTP {exc.response.status_code}: {detail}") from exc
        except LLMReasoningError:
            raise
        except (httpx.HTTPError, KeyError, json.JSONDecodeError, TypeError) as exc:
            raise LLMReasoningError(f"LLM reasoning failed: {type(exc).__name__}") from exc


llm_reasoning_service = LLMReasoningService()
