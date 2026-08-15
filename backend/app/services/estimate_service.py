from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP
from typing import Any

from app.db.models import Startup


def _money(value: Decimal) -> str:
    return str(value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def build_planning_estimates(startup: Startup, research: dict[str, Any] | None = None) -> dict[str, Any]:
    budget = Decimal(str(startup.budget))
    days = max(7, int(startup.time_horizon_days or 30))
    interview_target = max(8, min(30, round(days / 3)))
    pilot_target = max(15, min(60, round(days * 0.8)))
    validation_budget = budget * Decimal("0.40")
    acquisition_test_budget = budget * Decimal("0.30")
    reserve_budget = budget - validation_budget - acquisition_test_budget
    estimated_findings = [
        {
            "text": f"Planning hypothesis: a {pilot_target}-person pilot is a reasonable first validation cohort for the stated {days}-day horizon.",
            "category": "pilot_design",
            "number_type": "modeled_estimate",
            "confidence": "low",
            "methodology": "Capped planning heuristic: 0.8 participants per day, bounded to 15-60 participants.",
            "assumptions": ["This is a planning target, not observed demand.", "The team can recruit participants through the stated target market."],
            "validation_plan": "Recruit a smaller first cohort, measure activation, then revise the target using observed recruitment rate.",
        },
        {
            "text": f"Planning hypothesis: conduct {interview_target} qualified customer interviews before committing to paid acquisition.",
            "category": "customer_validation",
            "number_type": "modeled_estimate",
            "confidence": "low",
            "methodology": "One interview target per three days of the stated horizon, bounded to 8-30 interviews.",
            "assumptions": ["Interviews are available in the target market.", "A qualified interview includes the target customer and a real career problem."],
            "validation_plan": "Track completed interviews, recurring pain points, and willingness to try the core workflow.",
        },
        {
            "text": "Planning hypothesis: the first acquisition test should compare at least two channels before scaling.",
            "category": "channel_validation",
            "number_type": "modeled_estimate",
            "confidence": "low",
            "methodology": "Experimental design recommendation; no external CAC or conversion claim is assumed.",
            "assumptions": ["Two channels can be tested without changing the product promise.", "Success is judged by qualified activation, not clicks alone."],
            "validation_plan": "Use equal test windows and compare qualified activation and follow-up interview rate.",
        },
    ]
    numeric_claims = [
        {
            "label": "Validation interview target",
            "value": str(interview_target),
            "unit": "interviews",
            "currency": None,
            "geography": startup.target_market,
            "period": f"First {days} days",
            "number_type": "modeled_estimate",
            "source_ids": [],
            "methodology": "One interview target per three days, bounded to 8-30.",
            "confidence": "low",
            "assumptions": ["Planning target only; not a market statistic."],
            "validation_plan": "Replace with the observed completion rate after the first recruitment cycle.",
        },
        {
            "label": "Pilot cohort target",
            "value": str(pilot_target),
            "unit": "participants",
            "currency": None,
            "geography": startup.target_market,
            "period": f"First {days} days",
            "number_type": "modeled_estimate",
            "source_ids": [],
            "methodology": "0.8 participants per day, bounded to 15-60.",
            "confidence": "low",
            "assumptions": ["Planning target only; not observed demand."],
            "validation_plan": "Update after measuring weekly recruitment and activation.",
        },
        {
            "label": "Validation work budget allocation",
            "value": _money(validation_budget),
            "unit": "budget units",
            "currency": startup.currency,
            "geography": startup.target_market,
            "period": f"First {days} days",
            "number_type": "modeled_estimate",
            "source_ids": [],
            "methodology": "40% of the user-provided startup budget reserved for interviews, pilots, and product validation.",
            "confidence": "low",
            "assumptions": ["The startup budget is user-provided context.", "40% is a planning allocation, not a market-derived ratio."],
            "validation_plan": "Review spend weekly and change the allocation after evidence from the first experiments.",
        },
        {
            "label": "Acquisition test budget allocation",
            "value": _money(acquisition_test_budget),
            "unit": "budget units",
            "currency": startup.currency,
            "geography": startup.target_market,
            "period": f"First {days} days",
            "number_type": "modeled_estimate",
            "source_ids": [],
            "methodology": "30% of the user-provided startup budget reserved for controlled channel tests.",
            "confidence": "low",
            "assumptions": ["No CAC or conversion rate is assumed.", "No spend occurs automatically."],
            "validation_plan": "Authorize spend only after a human reviews the test design and platform settings.",
        },
        {
            "label": "Contingency and iteration reserve",
            "value": _money(reserve_budget),
            "unit": "budget units",
            "currency": startup.currency,
            "geography": startup.target_market,
            "period": f"First {days} days",
            "number_type": "modeled_estimate",
            "source_ids": [],
            "methodology": "Remaining 30% of the user-provided startup budget.",
            "confidence": "low",
            "assumptions": ["Reserve is a planning choice, not a forecast."],
            "validation_plan": "Release reserve only after reviewing experiment results and evidence gaps.",
        },
    ]
    return {
        "estimate_mode": "transparent_planning_estimates",
        "generated_by": "rule_based_fallback_until_llm_estimator_is_configured",
        "estimate_confidence": "low",
        "estimated_findings": estimated_findings,
        "estimated_numeric_claims": numeric_claims,
        "estimate_assumptions": [
            "These are planning estimates and hypotheses, not verified market facts.",
            "No market size, competitor count, CAC, conversion rate, or employment outcome is claimed.",
            "Every estimate must be replaced or recalibrated with observed experiment data.",
        ],
        "validation_tasks": [
            "Interview target customers.",
            "Run a controlled pilot.",
            "Measure activation and repeat usage.",
            "Validate willingness to pay before setting subscription prices.",
        ],
    }


def add_planning_estimates(startup: Startup, research: dict[str, Any]) -> dict[str, Any]:
    fallback_estimates = build_planning_estimates(startup, research)
    research = dict(research)
    llm_findings = [item for item in research.get("estimated_findings", []) if isinstance(item, dict)]
    llm_claims = [item for item in research.get("estimated_numeric_claims", []) if isinstance(item, dict)]
    estimates = {
        "estimate_mode": "llm_assisted_estimates" if (llm_findings or llm_claims) else fallback_estimates["estimate_mode"],
        "generated_by": "Manus API structured LLM output" if (llm_findings or llm_claims) else fallback_estimates["generated_by"],
        "estimated_findings": llm_findings or fallback_estimates["estimated_findings"],
        "estimated_numeric_claims": llm_claims or fallback_estimates["estimated_numeric_claims"],
        "estimate_assumptions": research.get("estimate_assumptions") or fallback_estimates["estimate_assumptions"],
        "validation_tasks": research.get("validation_tasks") or fallback_estimates["validation_tasks"],
        "estimate_confidence": "low",
    }
    research["estimate_mode"] = estimates["estimate_mode"]
    research["generated_by"] = estimates["generated_by"]
    research["estimated_findings"] = estimates["estimated_findings"]
    research["estimated_numeric_claims"] = estimates["estimated_numeric_claims"]
    existing_claims = [claim for claim in research.get("numeric_claims", []) if not isinstance(claim, dict) or claim.get("number_type") != "modeled_estimate"]
    research["numeric_claims"] = existing_claims + estimates["estimated_numeric_claims"]
    if not research.get("market_overview") or str(research.get("market_overview")).lower().startswith("unknown"):
        research["market_overview"] = (
            "Preliminary planning view: the opportunity should be validated with customer interviews, "
            f"a {max(15, min(60, round(max(7, int(startup.time_horizon_days or 30)) * 0.8)))}-person pilot target, and controlled channel experiments. "
            "This is a modeled planning hypothesis, not a verified market-size claim."
        )
        research["market_overview_status"] = "modeled_estimate"
    research["estimate_assumptions"] = estimates["estimate_assumptions"]
    research["validation_tasks"] = estimates["validation_tasks"]
    quality = dict(research.get("data_quality") or {})
    quality["estimate_confidence"] = estimates["estimate_confidence"]
    quality["estimated_numeric_claims"] = len(estimates["estimated_numeric_claims"])
    quality["verified_numeric_claims"] = len(research.get("numeric_claims") or [])
    research["data_quality"] = quality
    return research
