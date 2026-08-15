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
    if not competitors:
        competitors = [
            {"name": "University career services", "classification": "indirect", "strength": "Institutional trust and access to students are plausible competitive advantages.", "weakness": "Capacity, coverage, and quality are not verified for this startup.", "pricing": "Usually free or subsidized to eligible students; verify locally.", "source_ids": [], "evidence_status": "modeled_estimate"},
            {"name": "Local job boards and recruitment platforms", "classification": "indirect", "strength": "They may have employer distribution and job inventory.", "weakness": "A personalized coaching workflow is not assumed and must be verified.", "pricing": "Unknown; verify current public and employer pricing.", "source_ids": [], "evidence_status": "modeled_estimate"},
            {"name": "General-purpose AI assistants", "classification": "indirect", "strength": "Low-friction access and broad conversational capability.", "weakness": "Local career evidence, workflow continuity, and accountability are not assumed.", "pricing": "Unknown for the relevant user segment.", "source_ids": [], "evidence_status": "modeled_estimate"},
        ]
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
    estimates = _insight_items(research, "estimated_findings")
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
        ] or [{"text": item.get("text"), "basis": "planning_estimate", "source_ids": [], "evidence_status": "modeled_estimate"} for item in estimates if item.get("category") in {"pilot_design", "customer_validation"}] or [{"text": "Modeled planning opportunity: validate demand before scaling.", "basis": "planning_estimate", "source_ids": [], "evidence_status": "modeled_estimate"}],
        "threats": [
            {"text": item.get("text"), "basis": "research", "source_ids": _source_ids(item) if has_snapshot else [], "evidence_status": "source_backed" if has_snapshot else "unknown"}
            for item in threats
        ] or [{"text": item.get("text"), "basis": "planning_estimate", "source_ids": [], "evidence_status": "modeled_estimate"} for item in estimates if item.get("category") == "channel_validation"] or [{"text": "Modeled planning threat: scaling before validating acquisition economics may waste budget.", "basis": "planning_estimate", "source_ids": [], "evidence_status": "modeled_estimate"}],
        "sources": research.get("sources", []) if has_snapshot else [],
        "data_quality": _research_quality(research),
    }


def marketing_plan(startup: Startup, research: dict[str, Any], swot: dict[str, Any]) -> dict[str, Any]:
    has_snapshot = bool(research.get("snapshot_id"))
    estimated_claims = {claim.get("label"): claim for claim in research.get("estimated_numeric_claims", []) if isinstance(claim, dict)}
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
            "amount_allocations": {
                "validation": estimated_claims.get("Validation work budget allocation", {}).get("value"),
                "acquisition_test": estimated_claims.get("Acquisition test budget allocation", {}).get("value"),
                "reserve": estimated_claims.get("Contingency and iteration reserve", {}).get("value"),
            },
            "status": "modeled_estimate",
            "reason": "Planning allocation derived from the user-provided budget using an explicit 40/30/30 heuristic; it is not a market price or forecast.",
        },
        "kpis": [
            {"name": "Qualified student interviews", "target": estimated_claims.get("Validation interview target", {}).get("value"), "target_type": "modeled_estimate", "definition": "Completed interviews with the target customer segment."},
            {"name": "Pilot participants", "target": estimated_claims.get("Pilot cohort target", {}).get("value"), "target_type": "modeled_estimate", "definition": "Participants activated in a controlled validation cohort."},
            {"name": "Activation", "target": "Measure before setting a target", "target_type": "validation_required", "definition": "A user completes the core diagnostic or coaching workflow."},
            {"name": "Repeat usage", "target": "Measure before setting a target", "target_type": "validation_required", "definition": "A user returns for a second meaningful coaching task."},
            {"name": "Partner validation", "target": "1 pilot conversation", "target_type": "modeled_estimate", "definition": "A university, career center, or program agrees to a pilot."}
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
