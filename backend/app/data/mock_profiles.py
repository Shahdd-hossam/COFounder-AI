from __future__ import annotations

from copy import deepcopy
from typing import Any


CAREER_SOURCES = [
    {"id": "mock_ilo_employability", "title": "ILO employability and graduate transition reference", "publisher": "Mock reference profile", "url": "https://www.ilo.org/skills-and-lifelong-learning", "retrieved_on": "2026-08-15", "quality": "medium", "source_type": "mock_reference"},
    {"id": "mock_university_career_centers", "title": "University career-center and employability programs", "publisher": "Mock reference profile", "url": "https://www.aucegypt.edu/career-center", "retrieved_on": "2026-08-15", "quality": "medium", "source_type": "mock_reference"},
    {"id": "mock_job_platforms", "title": "Local job-board and early-career platform landscape", "publisher": "Mock reference profile", "url": "https://www.wuzzuf.net/", "retrieved_on": "2026-08-15", "quality": "medium", "source_type": "mock_reference"},
]

CAREER_PAYLOAD: dict[str, Any] = {
    "market_overview": "Mock research baseline: localized career-coaching products serve a large and recurring university-to-employment problem. The strongest initial wedge is a bilingual workflow that combines career direction, CV improvement, interview practice, and accountable next steps. Validate the baseline with local interviews and a pilot before treating any planning number as demand evidence.",
    "market_overview_source_ids": ["mock_ilo_employability", "mock_university_career_centers", "mock_job_platforms"],
    "target_customer_insights": [
        {"text": "Final-year students and recent graduates need a clearer bridge from academic background to practical job preparation.", "source_ids": ["mock_ilo_employability"], "confidence": "medium", "evidence_status": "mock_reference"},
        {"text": "A bilingual Arabic-English workflow is a plausible differentiator for students who need both local context and professional English outputs.", "source_ids": ["mock_university_career_centers"], "confidence": "medium", "evidence_status": "mock_reference"},
        {"text": "University partnerships can reduce acquisition friction and improve trust during early validation.", "source_ids": ["mock_university_career_centers"], "confidence": "medium", "evidence_status": "mock_reference"},
    ],
    "market_trends": [
        {"text": "Career platforms are moving from static job listings toward coaching, assessment, and resume/interview workflows.", "source_ids": ["mock_job_platforms"], "confidence": "medium", "evidence_status": "mock_reference"},
        {"text": "Employability programs increasingly combine digital guidance with institutional career services.", "source_ids": ["mock_ilo_employability", "mock_university_career_centers"], "confidence": "medium", "evidence_status": "mock_reference"},
    ],
    "customer_pain_points": [
        {"text": "Students are unsure which roles fit their skills and degree path.", "source_ids": ["mock_ilo_employability"], "confidence": "medium", "evidence_status": "mock_reference"},
        {"text": "CV quality, interview confidence, and consistent job-search execution are common workflow gaps.", "source_ids": ["mock_university_career_centers"], "confidence": "medium", "evidence_status": "mock_reference"},
    ],
    "competitors": [
        {"name": "University career services", "strength": "Institutional trust, access to students, and human support.", "weakness": "Limited personalized capacity and inconsistent follow-up at scale.", "pricing": "Usually free or subsidized to eligible students; verify locally.", "source_ids": ["mock_university_career_centers"], "evidence_status": "mock_reference"},
        {"name": "Local job boards and recruitment platforms", "strength": "Employer distribution, job inventory, and recruiter relationships.", "weakness": "Job matching may not provide a complete personalized coaching loop.", "pricing": "Job-seeker pricing varies; employer pricing requires current verification.", "source_ids": ["mock_job_platforms"], "evidence_status": "mock_reference"},
        {"name": "General-purpose AI assistants", "strength": "Low-friction, broad conversational help for resumes and interview questions.", "weakness": "Weak local evidence, progress tracking, and accountability unless specifically designed.", "pricing": "Varies by provider; no segment-specific price assumed.", "source_ids": [], "evidence_status": "modeled_estimate"},
    ],
    "opportunities": [
        {"text": "Own the bilingual career-readiness workflow for a focused university segment before expanding geography.", "source_ids": ["mock_university_career_centers"], "confidence": "medium", "evidence_status": "mock_reference"},
        {"text": "Partner with career centers, student organizations, and employability programs for distribution.", "source_ids": ["mock_university_career_centers", "mock_ilo_employability"], "confidence": "medium", "evidence_status": "mock_reference"},
    ],
    "threats": [
        {"text": "Free university support and general-purpose AI alternatives may reduce willingness to pay.", "source_ids": ["mock_university_career_centers"], "confidence": "medium", "evidence_status": "mock_reference"},
        {"text": "Job boards and established career platforms may have stronger employer distribution.", "source_ids": ["mock_job_platforms"], "confidence": "medium", "evidence_status": "mock_reference"},
    ],
    "sources": CAREER_SOURCES,
    "numeric_claims": [],
    "missing_fields": ["verified local willingness to pay", "verified CAC", "verified conversion rate", "validated employment outcome"],
    "conflicts": [],
    "assumptions": ["This is a coherent mock reference profile for product prototyping, not live market evidence.", "All planning numbers must be validated through experiments."],
    "data_mode": "mock_seed",
    "profile_family": "career_coach",
}

GENERIC_PAYLOAD: dict[str, Any] = {
    "market_overview": "Mock research baseline: the opportunity should be evaluated through a narrow customer segment, a repeatable pain point, and a measurable pilot. The initial strategy is to validate problem intensity and activation before scaling acquisition or pricing.",
    "market_overview_source_ids": ["mock_generic_validation"],
    "target_customer_insights": [{"text": "The strongest first customer is the segment with the most frequent, expensive, or urgent version of the described problem.", "source_ids": ["mock_generic_validation"], "confidence": "low", "evidence_status": "mock_reference"}],
    "market_trends": [{"text": "Digital products compete on distribution, workflow convenience, trust, and measurable outcomes rather than feature count alone.", "source_ids": ["mock_generic_validation"], "confidence": "low", "evidence_status": "mock_reference"}],
    "customer_pain_points": [{"text": "Customers may struggle with fragmented tools, uncertain outcomes, and the effort required to change existing behavior.", "source_ids": ["mock_generic_validation"], "confidence": "low", "evidence_status": "mock_reference"}],
    "competitors": [
        {"name": "Manual or incumbent workflow", "strength": "Existing trust and established behavior.", "weakness": "Often slower, less personalized, or more expensive to operate.", "pricing": "Unknown; verify in the target market.", "source_ids": ["mock_generic_validation"], "evidence_status": "mock_reference"},
        {"name": "Specialized local alternatives", "strength": "Local context and focused customer relationships.", "weakness": "Potentially limited automation or geographic coverage.", "pricing": "Unknown; verify current offers.", "source_ids": ["mock_generic_validation"], "evidence_status": "mock_reference"},
        {"name": "General-purpose AI tools", "strength": "Broad capability and low setup friction.", "weakness": "Limited domain-specific workflow, provenance, and accountability.", "pricing": "Varies by provider; no segment-specific price assumed.", "source_ids": [], "evidence_status": "modeled_estimate"},
    ],
    "opportunities": [{"text": "Start with one high-intent segment and a measurable workflow outcome.", "source_ids": ["mock_generic_validation"], "confidence": "low", "evidence_status": "mock_reference"}],
    "threats": [{"text": "Low switching costs and free alternatives can make retention difficult before the product proves a clear outcome.", "source_ids": ["mock_generic_validation"], "confidence": "low", "evidence_status": "mock_reference"}],
    "sources": [{"id": "mock_generic_validation", "title": "General startup validation reference profile", "publisher": "Mock reference profile", "url": "https://www.ycombinator.com/library/4A-a-guide-to-startup-ideas", "retrieved_on": "2026-08-15", "quality": "low", "source_type": "mock_reference"}],
    "numeric_claims": [],
    "missing_fields": ["verified market size", "verified competitor pricing", "verified customer demand", "verified CAC", "verified conversion rate"],
    "conflicts": [],
    "assumptions": ["This is a coherent mock reference profile for product prototyping, not live market evidence.", "Similarity matching selects a starting hypothesis and does not prove market fit."],
    "data_mode": "mock_seed",
    "profile_family": "generic",
}

PROFILES = [
    {"profile_key": "career_coach_egypt", "display_name": "Egypt / MENA career coaching", "keywords": ["career", "student", "students", "graduate", "university", "job", "jobs", "resume", "cv", "interview", "employability", "arabic", "english", "egypt", "alexandria"], "payload": CAREER_PAYLOAD, "priority": 100},
    {"profile_key": "marketplace_retail", "display_name": "Marketplace / retail platform", "keywords": ["marketplace", "buyers", "sellers", "retail", "ecommerce", "e-commerce", "products", "store", "delivery", "merchant"], "payload": GENERIC_PAYLOAD, "priority": 60},
    {"profile_key": "b2b_saas", "display_name": "B2B SaaS workflow", "keywords": ["b2b", "software", "saas", "teams", "workflow", "automation", "business", "subscription", "dashboard", "operations"], "payload": GENERIC_PAYLOAD, "priority": 55},
    {"profile_key": "fintech", "display_name": "Fintech / payments", "keywords": ["fintech", "payments", "wallet", "finance", "banking", "lending", "money", "transactions", "credit"], "payload": GENERIC_PAYLOAD, "priority": 55},
    {"profile_key": "healthcare", "display_name": "Healthcare platform", "keywords": ["health", "healthcare", "patient", "clinic", "doctor", "medical", "wellness", "hospital"], "payload": GENERIC_PAYLOAD, "priority": 55},
    {"profile_key": "generic_startup", "display_name": "General startup validation", "keywords": ["startup", "platform", "app", "mobile", "online", "ai", "service", "technology"], "payload": GENERIC_PAYLOAD, "priority": 1},
]


def profile_seed_rows() -> list[dict[str, Any]]:
    return [{"profile_key": item["profile_key"], "display_name": item["display_name"], "keywords": item["keywords"], "payload": deepcopy(item["payload"]), "priority": item["priority"]} for item in PROFILES]
