import sys
from pathlib import Path

BACKEND_PATH = Path(__file__).resolve().parents[1] / "backend"
if str(BACKEND_PATH) not in sys.path:
    sys.path.insert(0, str(BACKEND_PATH))

from app.services.evidence_cleaner import clean_research_payload


def test_source_reported_claim_without_source_becomes_unknown() -> None:
    result = clean_research_payload(
        {
            "market_overview": "A market exists.",
            "sources": [],
            "numeric_claims": [
                {
                    "label": "Market size",
                    "value": 123456,
                    "unit": "users",
                    "number_type": "source_reported",
                    "source_ids": [],
                }
            ],
        }
    )

    claim = result["numeric_claims"][0]
    assert claim["number_type"] == "unknown"
    assert claim["value"] is None
    assert result["data_quality"]["unknown_numeric_claims"] == 1


def test_valid_source_backed_claim_is_preserved() -> None:
    result = clean_research_payload(
        {
            "sources": [{"id": "src-1", "title": "Official report", "url": "https://example.com/report"}],
            "numeric_claims": [
                {
                    "label": "Reported users",
                    "value": 1200,
                    "unit": "users",
                    "number_type": "source_reported",
                    "source_ids": ["src-1"],
                    "confidence": "medium",
                }
            ],
        }
    )

    claim = result["numeric_claims"][0]
    assert claim["number_type"] == "source_reported"
    assert claim["value"] == "1200"
    assert claim["source_ids"] == ["src-1"]


def test_modeled_estimate_without_methodology_becomes_unknown() -> None:
    result = clean_research_payload(
        {
            "sources": [{"id": "src-1", "title": "Official report", "url": "https://example.com/report"}],
            "numeric_claims": [
                {
                    "label": "Estimated reachable users",
                    "value": 900,
                    "number_type": "modeled_estimate",
                    "source_ids": ["src-1"],
                }
            ],
        }
    )

    claim = result["numeric_claims"][0]
    assert claim["number_type"] == "unknown"
    assert claim["value"] is None


def test_uncited_textual_findings_are_not_returned_as_facts() -> None:
    result = clean_research_payload(
        {
            "market_overview": "The market is growing rapidly.",
            "market_trends": [{"text": "Demand is rising", "source_ids": []}],
            "competitors": [{"name": "Example competitor", "source_ids": []}],
            "sources": [],
        }
    )

    assert result["market_overview"].startswith("Unknown:")
    assert result["market_trends"] == []
    assert result["competitors"] == []
    assert result["data_quality"]["cleaning_issues"]
