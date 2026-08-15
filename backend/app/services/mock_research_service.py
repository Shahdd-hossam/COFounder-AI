from __future__ import annotations

import re
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import MockResearchProfile, Startup
from app.data.mock_profiles import profile_seed_rows

TOKEN_RE = re.compile(r"[a-z0-9]+", re.IGNORECASE)
STOP_WORDS = {"the", "and", "for", "with", "from", "that", "this", "into", "your", "their", "our", "are", "is", "an", "a", "to", "of", "in", "on", "by"}


def tokens(text: str) -> set[str]:
    return {token for token in TOKEN_RE.findall(text.lower()) if token not in STOP_WORDS and len(token) > 2}


def startup_query_text(startup: Startup) -> str:
    return " ".join([startup.name, startup.description, startup.target_customer, startup.target_market, startup.business_model, startup.goal, startup.language])


def seed_mock_profiles(db: Session) -> int:
    existing = {row.profile_key for row in db.scalars(select(MockResearchProfile)).all()}
    inserted = 0
    for row in profile_seed_rows():
        if row["profile_key"] in existing:
            continue
        db.add(MockResearchProfile(profile_key=row["profile_key"], display_name=row["display_name"], keywords_json=row["keywords"], payload_json=row["payload"], priority=row["priority"], enabled=True))
        inserted += 1
    if inserted:
        db.flush()
    return inserted


def match_profile(db: Session, startup: Startup) -> tuple[dict[str, Any], dict[str, Any]]:
    query_tokens = tokens(startup_query_text(startup))
    profiles = list(db.scalars(select(MockResearchProfile).where(MockResearchProfile.enabled.is_(True))).all())
    if not profiles:
        seed_mock_profiles(db)
        profiles = list(db.scalars(select(MockResearchProfile).where(MockResearchProfile.enabled.is_(True))).all())
    ranked: list[tuple[float, MockResearchProfile]] = []
    for profile in profiles:
        keyword_tokens = tokens(" ".join(profile.keywords_json or []))
        overlap = query_tokens.intersection(keyword_tokens)
        normalized = len(overlap) / max(1, len(keyword_tokens))
        query_coverage = len(overlap) / max(1, min(len(query_tokens), 10))
        score = round((normalized * 0.45) + (query_coverage * 0.45) + (min(profile.priority, 100) / 1000), 4)
        ranked.append((score, profile))
    ranked.sort(key=lambda item: (item[0], item[1].priority), reverse=True)
    score, selected = ranked[0]
    payload = dict(selected.payload_json or {})
    payload["data_mode"] = "mock_seed"
    payload["mock_profile_key"] = selected.profile_key
    payload["mock_profile_name"] = selected.display_name
    payload["similarity"] = {
        "score": score,
        "matched_keywords": sorted(query_tokens.intersection(tokens(" ".join(selected.keywords_json or [])))),
        "query_tokens": sorted(query_tokens),
        "profile_keywords": sorted(tokens(" ".join(selected.keywords_json or []))),
        "method": "token_overlap_with_priority",
    }
    quality = dict(payload.get("data_quality") or {})
    quality.update({"mock_profile_match": selected.display_name, "mock_similarity_score": score, "mock_data_notice": "Mock seed data used because live research was unavailable. Validate before treating it as market evidence."})
    payload["assumptions"] = list(payload.get("assumptions") or []) + ["The profile was selected by similarity against the startup description and context fields; this is a starting hypothesis, not proof of market fit."]
    payload["data_quality"] = quality
    return payload, {"profile_key": selected.profile_key, "display_name": selected.display_name, "score": score, "matched_keywords": sorted(query_tokens.intersection(tokens(" ".join(selected.keywords_json or []))))}
