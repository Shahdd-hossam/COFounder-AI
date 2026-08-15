from __future__ import annotations

from typing import Any


class MCPToolUnavailable(RuntimeError):
    pass


class MCPToolInvalidResponse(RuntimeError):
    pass


def normalize_tavily_result(raw: Any) -> dict[str, Any]:
    """Normalize an already-invoked Tavily MCP result.

    Direct MCP calls must be made by the approved runtime connector and then
    injected into the gateway. This module intentionally does not shell out or
    execute connector commands from the web process.
    """
    if not isinstance(raw, dict):
        raise MCPToolInvalidResponse("The Tavily MCP result must be a JSON object")
    if isinstance(raw.get("result"), dict):
        raw = raw["result"]
    return raw


def register_tavily_result(gateway: Any, raw_result: dict[str, Any]) -> None:
    """Register one verified, already-fetched result for a single workflow run.

    Production code should use a connector-aware runtime to invoke Tavily and
    pass its JSON result here. The gateway still performs all source and claim
    validation before persistence.
    """
    normalized = normalize_tavily_result(raw_result)

    async def handler(_: dict[str, Any]) -> dict[str, Any]:
        return normalized

    gateway.register("market_research", handler)
