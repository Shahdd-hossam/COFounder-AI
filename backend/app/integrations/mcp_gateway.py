from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Awaitable, Callable

from app.services.evidence_cleaner import clean_research_payload


@dataclass(frozen=True)
class ToolResult:
    feature: str
    status: str
    tool: str | None
    result: dict[str, Any]
    evidence: list[dict[str, Any]]
    assumptions: list[str]
    missing_fields: list[str]
    error: str | None = None
    completed_at: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "feature": self.feature,
            "status": self.status,
            "tool": self.tool,
            "result": self.result,
            "evidence": self.evidence,
            "data_quality": {
                "missing_fields": self.missing_fields,
                "assumptions": self.assumptions,
            },
            "error": self.error,
            "completed_at": self.completed_at or datetime.now(timezone.utc).isoformat(),
        }


class MCPGateway:
    """Feature-neutral boundary for verified MCP tools.

    Concrete MCP calls are intentionally injected. This prevents React and
    feature services from depending on provider-specific tool names and keeps
    the application usable when a connector is unavailable.
    """

    def __init__(self) -> None:
        self._tools: dict[str, Callable[[dict[str, Any]], Awaitable[dict[str, Any]]]] = {}

    def register(self, feature: str, handler: Callable[[dict[str, Any]], Awaitable[dict[str, Any]]]) -> None:
        self._tools[feature] = handler

    async def run(self, feature: str, payload: dict[str, Any], fallback: dict[str, Any]) -> ToolResult:
        handler = self._tools.get(feature)
        safe_fallback = clean_research_payload(fallback) if feature == "market_research" else fallback
        if handler is None:
            return ToolResult(
                feature=feature,
                status="fallback",
                tool=None,
                result=safe_fallback,
                evidence=safe_fallback.get("sources", []) if feature == "market_research" else [],
                assumptions=["No approved MCP tool is configured for this feature."],
                missing_fields=safe_fallback.get("data_quality", {}).get("missing_fields", []) if feature == "market_research" else [],
            )

        try:
            response = await handler(payload)
            safe_response = clean_research_payload(response) if feature == "market_research" else response
            quality = safe_response.get("data_quality", {}) if feature == "market_research" else {}
            return ToolResult(
                feature=feature,
                status="success",
                tool=feature,
                result=safe_response,
                evidence=safe_response.get("sources", response.get("evidence", [])) if feature == "market_research" else response.get("evidence", []),
                assumptions=quality.get("assumptions", response.get("assumptions", [])),
                missing_fields=quality.get("missing_fields", response.get("missing_fields", [])),
            )
        except Exception as exc:  # provider-specific failures become data
            return ToolResult(
                feature=feature,
                status="failed",
                tool=feature,
                result=safe_fallback,
                evidence=[],
                assumptions=["The configured tool failed; fallback output is not verified research."],
                missing_fields=safe_fallback.get("data_quality", {}).get("missing_fields", []) if feature == "market_research" else [],
                error=str(exc),
            )


mcp_gateway = MCPGateway()
