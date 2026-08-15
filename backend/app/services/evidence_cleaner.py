from __future__ import annotations

from datetime import date
from decimal import Decimal, InvalidOperation
from typing import Any
from urllib.parse import urlparse


ALLOWED_NUMBER_TYPES = {
    "source_reported",
    "derived_from_sources",
    "modeled_estimate",
    "unknown",
}


def _valid_url(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def _as_decimal(value: Any) -> Decimal | None:
    if value is None or value == "":
        return None
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError):
        return None


def clean_evidence(raw_sources: Any) -> tuple[list[dict[str, Any]], list[str]]:
    cleaned: list[dict[str, Any]] = []
    issues: list[str] = []
    seen_ids: set[str] = set()

    for index, source in enumerate(raw_sources if isinstance(raw_sources, list) else []):
        if not isinstance(source, dict):
            issues.append(f"sources[{index}] ignored: source is not an object")
            continue
        url = source.get("url")
        if not _valid_url(url):
            issues.append(f"sources[{index}] ignored: URL is missing or invalid")
            continue
        source_id = str(source.get("id") or f"source-{len(cleaned) + 1}")
        if source_id in seen_ids:
            issues.append(f"sources[{index}] ignored: duplicate source id {source_id}")
            continue
        seen_ids.add(source_id)
        cleaned.append(
            {
                "id": source_id,
                "title": str(source.get("title") or "Untitled source"),
                "publisher": source.get("publisher"),
                "url": url,
                "retrieved_on": source.get("retrieved_on") or date.today().isoformat(),
                "quality": source.get("quality") if source.get("quality") in {"low", "medium", "high"} else "low",
            }
        )

    return cleaned, issues


def clean_numeric_claims(raw_claims: Any, source_ids: set[str]) -> tuple[list[dict[str, Any]], list[str]]:
    cleaned: list[dict[str, Any]] = []
    issues: list[str] = []

    for index, claim in enumerate(raw_claims if isinstance(raw_claims, list) else []):
        if not isinstance(claim, dict):
            issues.append(f"numeric_claims[{index}] ignored: claim is not an object")
            continue

        label = str(claim.get("label") or "").strip()
        number_type = str(claim.get("number_type") or "unknown")
        value = _as_decimal(claim.get("value"))
        linked_sources = [str(item) for item in claim.get("source_ids", []) if str(item) in source_ids]

        if not label:
            issues.append(f"numeric_claims[{index}] ignored: label is missing")
            continue
        if number_type not in ALLOWED_NUMBER_TYPES:
            issues.append(f"numeric_claims[{index}] downgraded: unknown number_type")
            number_type = "unknown"
        if number_type in {"source_reported", "derived_from_sources"} and not linked_sources:
            issues.append(f"numeric_claims[{index}] downgraded: source-backed claim has no valid source")
            number_type = "unknown"
            value = None
        if number_type == "modeled_estimate" and not claim.get("methodology"):
            issues.append(f"numeric_claims[{index}] downgraded: modeled estimate has no methodology")
            number_type = "unknown"
            value = None
        if number_type != "unknown" and value is None:
            issues.append(f"numeric_claims[{index}] downgraded: numeric value is invalid")
            number_type = "unknown"

        cleaned.append(
            {
                "label": label,
                "value": str(value) if value is not None else None,
                "unit": claim.get("unit"),
                "currency": claim.get("currency"),
                "geography": claim.get("geography"),
                "period": claim.get("period"),
                "number_type": number_type,
                "source_ids": linked_sources,
                "methodology": claim.get("methodology"),
                "confidence": claim.get("confidence") if claim.get("confidence") in {"low", "medium", "high"} else "low",
                "assumptions": [str(item) for item in claim.get("assumptions", [])],
            }
        )

    return cleaned, issues


ALLOWED_UNSOURCED_STATUSES = {"mock_reference", "modeled_estimate", "llm_estimate", "context", "hypothesis"}


def _clean_insights(raw_items: Any, source_ids: set[str], field_name: str, issues: list[str]) -> list[dict[str, Any]]:
    cleaned: list[dict[str, Any]] = []
    for index, item in enumerate(raw_items if isinstance(raw_items, list) else []):
        if not isinstance(item, dict) or not str(item.get("text") or "").strip():
            issues.append(f"{field_name}[{index}] ignored: insight text is missing")
            continue
        linked_sources = [str(item_id) for item_id in item.get("source_ids", []) if str(item_id) in source_ids]
        evidence_status = str(item.get("evidence_status") or "")
        if not linked_sources and evidence_status not in ALLOWED_UNSOURCED_STATUSES:
            issues.append(f"{field_name}[{index}] ignored: insight has no valid source")
            continue
        cleaned.append({
            "text": str(item["text"]).strip(),
            "source_ids": linked_sources,
            "confidence": item.get("confidence") if item.get("confidence") in {"low", "medium", "high"} else "low",
            "evidence_status": evidence_status or ("source_backed" if linked_sources else "unknown"),
            "methodology": item.get("methodology"),
            "assumptions": [str(value) for value in item.get("assumptions", [])],
            "validation_plan": item.get("validation_plan"),
        })
    return cleaned


def _clean_competitors(raw_items: Any, source_ids: set[str], issues: list[str]) -> list[dict[str, Any]]:
    cleaned: list[dict[str, Any]] = []
    for index, item in enumerate(raw_items if isinstance(raw_items, list) else []):
        if not isinstance(item, dict) or not str(item.get("name") or "").strip():
            issues.append(f"competitors[{index}] ignored: competitor name is missing")
            continue
        linked_sources = [str(item_id) for item_id in item.get("source_ids", []) if str(item_id) in source_ids]
        evidence_status = str(item.get("evidence_status") or "")
        if not linked_sources and evidence_status not in ALLOWED_UNSOURCED_STATUSES:
            issues.append(f"competitors[{index}] ignored: competitor has no valid source")
            continue
        cleaned.append({
            "name": str(item["name"]).strip(),
            "strength": item.get("strength"),
            "weakness": item.get("weakness"),
            "pricing": item.get("pricing"),
            "source_ids": linked_sources,
            "evidence_status": evidence_status or ("source_backed" if linked_sources else "unknown"),
            "reason": item.get("reason"),
        })
    return cleaned


def clean_research_payload(raw: Any) -> dict[str, Any]:
    payload = raw if isinstance(raw, dict) else {}
    sources, source_issues = clean_evidence(payload.get("sources", payload.get("evidence", [])))
    source_ids = {item["id"] for item in sources}
    numeric_claims, claim_issues = clean_numeric_claims(payload.get("numeric_claims", []), source_ids)
    issues = source_issues + claim_issues

    reported_quality = payload.get("data_quality") if isinstance(payload.get("data_quality"), dict) else {}
    overview = payload.get("market_overview")
    overview_source_ids = [str(item_id) for item_id in payload.get("market_overview_source_ids", []) if str(item_id) in source_ids]
    if overview and not str(overview).startswith("Unknown:") and not overview_source_ids:
        issues.append("market_overview downgraded: no valid source_ids")
        overview = "Unknown: the market overview was returned without a valid citation."
    insight_fields = {
        "target_customer_insights": _clean_insights(payload.get("target_customer_insights"), source_ids, "target_customer_insights", issues),
        "market_trends": _clean_insights(payload.get("market_trends"), source_ids, "market_trends", issues),
        "customer_pain_points": _clean_insights(payload.get("customer_pain_points"), source_ids, "customer_pain_points", issues),
        "opportunities": _clean_insights(payload.get("opportunities"), source_ids, "opportunities", issues),
        "threats": _clean_insights(payload.get("threats"), source_ids, "threats", issues),
    }
    quality = {
        "confidence": "high" if sources and not issues else "medium" if sources else "low",
        "coverage": 1.0 if sources and not issues else 0.5 if sources else 0.0,
        "missing_fields": payload.get("missing_fields") if isinstance(payload.get("missing_fields"), list) else reported_quality.get("missing_fields", []),
        "conflicts": payload.get("conflicts") if isinstance(payload.get("conflicts"), list) else reported_quality.get("conflicts", []),
        "assumptions": payload.get("assumptions") if isinstance(payload.get("assumptions"), list) else reported_quality.get("assumptions", []),
        "cleaning_issues": issues,
        "unknown_numeric_claims": sum(1 for claim in numeric_claims if claim["number_type"] == "unknown"),
    }
    for key in ("mock_profile_match", "mock_similarity_score", "mock_data_notice", "fallback_chain", "fallback_errors", "llm_reasoning", "estimate_confidence", "estimated_numeric_claims", "verified_numeric_claims"):
        if key in reported_quality:
            quality[key] = reported_quality[key]
    result = {
        "market_overview": overview or "Unknown: no verified market overview was returned.",
        "market_overview_source_ids": overview_source_ids,
        "target_customer_insights": insight_fields["target_customer_insights"],
        "competitors": _clean_competitors(payload.get("competitors"), source_ids, issues),
        "market_trends": insight_fields["market_trends"],
        "customer_pain_points": insight_fields["customer_pain_points"],
        "opportunities": insight_fields["opportunities"],
        "threats": insight_fields["threats"],
        "sources": sources,
        "numeric_claims": numeric_claims,
        "data_quality": quality,
    }
    for key in ("data_mode", "profile_family", "mock_profile_key", "mock_profile_name", "similarity", "llm_reasoning", "llm_estimate_mode", "estimated_findings", "estimated_numeric_claims", "estimate_mode", "generated_by", "estimate_assumptions", "validation_tasks", "llm_assumptions"):
        if key in payload:
            result[key] = payload[key]
    return result
