import os
import sys
from pathlib import Path

os.environ["DATABASE_URL"] = "sqlite:///./test_cofounder_ai_features.db"
os.environ["MANUS_ENABLED"] = "false"

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_PATH = PROJECT_ROOT / "backend"
if str(BACKEND_PATH) not in sys.path:
    sys.path.insert(0, str(BACKEND_PATH))

from fastapi.testclient import TestClient

from app.core.config import get_settings
from app.db.models import Base
from app.db.session import get_engine, reset_engine_for_tests
from app.main import app


def setup_module() -> None:
    get_settings.cache_clear()
    reset_engine_for_tests()
    Base.metadata.drop_all(bind=get_engine(get_settings()))
    Base.metadata.create_all(bind=get_engine(get_settings()))


def teardown_module() -> None:
    Base.metadata.drop_all(bind=get_engine(get_settings()))
    reset_engine_for_tests()


def create_startup(client: TestClient) -> dict:
    return client.post(
        "/api/v1/startups",
        json={
            "name": "growza",
            "description": "A bilingual AI career coach for final-year university students in Egypt.",
            "target_customer": "Final-year university students",
            "target_market": "Egypt, starting with Alexandria",
            "business_model": "Freemium subscription",
            "goal": "Acquire qualified beta users",
            "budget": 10000,
            "currency": "EGP",
            "time_horizon_days": 30,
            "language": "Arabic and English",
        },
    ).json()


def test_arbitrary_startup_uses_description_driven_fallback_safely() -> None:
    client = TestClient(app)
    startup = create_startup(client)

    research = client.post(f"/api/v1/startups/{startup['id']}/market-research/runs").json()
    assert research["status"] == "partial"
    result = research["result_json"]
    assert result["numeric_claims"] == []
    assert result["sources"] == []
    assert result["market_overview"].startswith("Unknown:")
    assert "Tavily/OpenRouter MCP" in result["data_quality"]["fallback_chain"]
    assert "Manus API" in result["data_quality"]["fallback_chain"]
    assert any("description" in assumption.lower() for assumption in result["data_quality"]["assumptions"])


def test_all_feature_runs_remain_execution_safe_without_evidence() -> None:
    client = TestClient(app)
    startup = create_startup(client)

    competitor = client.post(f"/api/v1/startups/{startup['id']}/competitor-analysis/runs").json()
    assert competitor["status"] == "partial"
    assert competitor["result_json"]["competitors"] == []

    swot = client.post(f"/api/v1/startups/{startup['id']}/swot/runs").json()
    assert swot["status"] == "partial"
    assert all(item["evidence_status"] in {"context", "hypothesis", "unknown"} for item in swot["result_json"]["strengths"] + swot["result_json"]["weaknesses"])

    marketing = client.post(f"/api/v1/startups/{startup['id']}/marketing-plan/runs").json()
    assert marketing["status"] == "partial"
    assert marketing["result_json"]["budget_guidance"]["amount_allocations"] is None
    assert marketing["result_json"]["kpis"][0]["target"] is None

    action_plan = client.post(f"/api/v1/startups/{startup['id']}/action-plans/runs").json()
    assert action_plan["status"] == "partial"
    assert action_plan["result_json"]["execution_enabled"] is False
    assert action_plan["result_json"]["budget"]["spend_authorized"] is False
