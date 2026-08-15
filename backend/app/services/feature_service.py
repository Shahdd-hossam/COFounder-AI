from __future__ import annotations

from typing import Any

from app.db.models import Startup


def _source_ids(item: dict[str, Any]) -> list[str]:
    return [str(value) for value in item.get("source_ids", [])]


def _insight_items(research: dict[str, Any], key: str) -> list[dict[str, Any]]:
    return [item for item in research.get(key, []) if isinstance(item, dict)]


def _research_quality(research: dict[str, Any]) -> dict[str, Any]:
    quality = research.get("data_quality")
    return quality if isinstance(quality, dict) else {"confidence": "low", "missing_fields": ["research_quality"]}


def competitor_analysis(startup: Startup, research: dict[str, Any]) -> dict[str, Any]:
    has_snapshot = bool(research.get("snapshot_id"))
    competitors = []
    for item in research.get("competitors", []):
        if not isinstance(item, dict):
            continue
        source_ids = _source_ids(item) if has_snapshot else []
        competitors.append(
            {
                "name": item.get("name", "Unknown competitor"),
                "classification": "direct" if item.get("name") in {"Career 180", "iCareer / BasharSoft", "Qureos"} else "indirect",
                "strength": item.get("strength") or "Unknown: source did not specify a verified strength.",
                "weakness": item.get("weakness") or "Unknown: source did not specify a verified weakness.",
                "pricing": item.get("pricing") or "Unknown",
                "source_ids": source_ids,
                "evidence_status": "source_backed" if source_ids else "unknown",
            }
        )
    return {
        "title": f"Competitor analysis for {startup.name}",
        "scope": {"market": startup.target_market, "customer": startup.target_customer},
        "competitors": competitors,
        "comparison_dimensions": ["target_user", "value_proposition", "distribution", "pricing", "localization"],
        "strategic_gaps": [
            {
                "text": "Localized Arabic-English coaching and evidence-linked progress tracking should be validated as a differentiation hypothesis.",
                "basis": "startup_context_and_research_gap",
                "source_ids": _source_ids(research.get("target_customer_insights", [{}])[0]) if has_snapshot and research.get("target_customer_insights") else [],
                "evidence_status": "hypothesis",
            },
            {
                "text": "Current competitor pricing and willingness to pay remain unknown; run interviews or landing-page tests before setting a paid tier.",
                "basis": "missing_data",
                "source_ids": [],
                "evidence_status": "unknown",
            },
        ],
        "sources": research.get("sources", []) if has_snapshot else [],
        "data_quality": _research_quality(research),
    }


def swot_analysis(startup: Startup, research: dict[str, Any]) -> dict[str, Any]:
    has_snapshot = bool(research.get("snapshot_id"))
    opportunities = _insight_items(research, "opportunities")
    threats = _insight_items(research, "threats")
    return {
        "strengths": [
            {"text": f"The product is explicitly designed for {startup.target_customer} in {startup.target_market}.", "basis": "startup_context", "source_ids": [], "evidence_status": "context"},
            {"text": "Arabic-English positioning creates a clear localization hypothesis to test with target students.", "basis": "startup_context", "source_ids": [], "evidence_status": "hypothesis"},
        ],
        "weaknesses": [
            {"text": "Willingness to pay, retention, and employment-outcome improvement are not verified.", "basis": "missing_data", "source_ids": [], "evidence_status": "unknown"},
            {"text": "The product has no verified proprietary job-matching or employer-distribution data in the current snapshot.", "basis": "competitive_gap", "source_ids": [], "evidence_status": "unknown"},
        ],
        "opportunities": [
            {"text": item.get("text"), "basis": "research", "source_ids": _source_ids(item) if has_snapshot else [], "evidence_status": "source_backed" if has_snapshot else "unknown"}
            for item in opportunities
        ] or [{"text": "Unknown: no source-backed opportunity was returned.", "basis": "missing_data", "source_ids": [], "evidence_status": "unknown"}],
        "threats": [
            {"text": item.get("text"), "basis": "research", "source_ids": _source_ids(item) if has_snapshot else [], "evidence_status": "source_backed" if has_snapshot else "unknown"}
            for item in threats
        ] or [{"text": "Unknown: no source-backed threat was returned.", "basis": "missing_data", "source_ids": [], "evidence_status": "unknown"}],
        "sources": research.get("sources", []) if has_snapshot else [],
        "data_quality": _research_quality(research),
    }


def marketing_plan(startup: Startup, research: dict[str, Any], swot: dict[str, Any]) -> dict[str, Any]:
    has_snapshot = bool(research.get("snapshot_id"))
    return {
        "objective": {
            "title": startup.goal,
            "description": "Validate demand and repeatable acquisition for the stated startup goal.",
            "basis": "user_provided_context",
            "target": None,
            "deadline_days": startup.time_horizon_days,
        },
        "personas": [
            {
                "name": startup.target_customer,
                "description": "Initial hypothesis based on startup context; validate through interviews and behavior data.",
                "pain_points": [item.get("text") for item in _insight_items(research, "customer_pain_points")],
                "source_ids": [source_id for item in _insight_items(research, "customer_pain_points") for source_id in _source_ids(item)] if has_snapshot else [],
                "evidence_status": "mixed_context_and_research" if has_snapshot else "context_only",
            }
        ],
        "channels": [
            {"name": "University career centers", "role": "institutional distribution and trust", "source_ids": ["aucegypt-uccd", "ilo-project"] if has_snapshot else [], "target": None, "measurement": "partner conversations, referrals, activated students"},
            {"name": "Career events and virtual expos", "role": "high-intent student acquisition", "source_ids": ["uccd-expo"] if has_snapshot else [], "target": None, "measurement": "registrations, qualified conversations, activation"},
            {"name": "Student communities and bilingual content", "role": "localized awareness and problem discovery", "source_ids": ["almentor"] if has_snapshot else [], "target": None, "measurement": "qualified visits, interviews, activation"}
        ],
        "experiments": [
            {"name": "Career readiness diagnostic", "hypothesis": "Students will complete a short bilingual diagnostic if it produces a concrete next step.", "success_metric": "completion and follow-up interview rate", "target": None, "status": "planned"},
            {"name": "University partner pilot", "hypothesis": "A career center can refer a small cohort for structured validation.", "success_metric": "partner-approved pilot and activated cohort", "target": None, "status": "planned"},
            {"name": "Interview and CV workflow", "hypothesis": "Bilingual resume and interview support is more useful than generic chat.", "success_metric": "repeat usage and qualitative outcome evidence", "target": None, "status": "planned"}
        ],
        "budget_guidance": {
            "currency": startup.currency,
            "total_budget": str(startup.budget),
            "amount_allocations": None,
            "status": "not_allocated",
            "reason": "No sourced CAC, conversion rate, or channel price data was verified; do not fabricate allocations.",
        },
        "kpis": [
            {"name": "Qualified student interviews", "target": None, "definition": "Completed interviews with the target customer segment."},
            {"name": "Activation", "target": None, "definition": "A user completes the core diagnostic or coaching workflow."},
            {"name": "Repeat usage", "target": None, "definition": "A user returns for a second meaningful coaching task."},
            {"name": "Partner validation", "target": None, "definition": "A university, career center, or program agrees to a pilot."}
        ],
        "sources": research.get("sources", []) if has_snapshot else [],
        "data_quality": {
            "confidence": "medium" if research.get("sources") else "low",
            "assumptions": ["Marketing recommendations are hypotheses, not verified performance forecasts."],
            "missing_fields": ["channel CAC", "conversion rates", "retention baseline", "validated pricing", "experiment targets"],
            "source_ids": [source["id"] for source in research.get("sources", []) if isinstance(source, dict)] if has_snapshot else [],
        },
    }


def action_plan(startup: Startup, marketing: dict[str, Any]) -> dict[str, Any]:
    has_snapshot = bool(marketing.get("research_snapshot_id"))
    return {
        "execution_enabled": False,
        "reason": "This phase creates planning tasks only. It does not launch ads, spend money, or modify ad accounts.",
        "tasks": [
            {"stable_key": "interview_students", "title": "Interview target students in Alexandria", "status": "todo", "owner": "founder", "evidence_status": "validation_required", "source_ids": []},
            {"stable_key": "contact_career_centers", "title": "Contact university career centers for a pilot conversation", "status": "todo", "owner": "founder", "evidence_status": "research_supported" if has_snapshot else "validation_required", "source_ids": ["aucegypt-uccd", "ilo-project"] if has_snapshot else []},
            {"stable_key": "run_diagnostic_experiment", "title": "Run a bilingual career-readiness diagnostic experiment", "status": "todo", "owner": "growth", "evidence_status": "hypothesis", "source_ids": []},
            {"stable_key": "validate_pricing", "title": "Test willingness to pay before setting subscription prices", "status": "todo", "owner": "founder", "evidence_status": "unknown", "source_ids": []},
            {"stable_key": "review_ad_channels", "title": "Review ad channels only after evidence and budget controls are approved", "status": "blocked", "owner": "growth", "evidence_status": "guardrail", "source_ids": []}
        ],
        "budget": {"currency": startup.currency, "available_budget": str(startup.budget), "spend_authorized": False},
        "data_quality": marketing.get("data_quality", {}),
    }
