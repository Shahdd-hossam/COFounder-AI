import os
import sys
from pathlib import Path

os.environ["DATABASE_URL"] = "sqlite:///./test_cofounder_ai_features.db"

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
            "name": "CareerLaunch Egypt",
            "description": "An Arabic-English AI career coach for final-year university students.",
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


def test_verified_snapshot_and_derived_workflows_preserve_evidence() -> None:
    client = TestClient(app)
    startup = create_startup(client)

    research = client.post(f"/api/v1/startups/{startup['id']}/market-research/runs").json()
    assert research["status"] == "ready"
    assert research["result_json"]["snapshot_id"].startswith("careerlaunch-egypt")
    assert research["result_json"]["numeric_claims"]
    assert all(claim["source_ids"] for claim in research["result_json"]["numeric_claims"])

    competitor = client.post(f"/api/v1/startups/{startup['id']}/competitor-analysis/runs").json()
    assert competitor["status"] == "ready"
    assert competitor["result_json"]["competitors"]
    assert all("pricing" in item for item in competitor["result_json"]["competitors"])

    swot = client.post(f"/api/v1/startups/{startup['id']}/swot/runs").json()
    assert swot["status"] == "ready"
    assert swot["result_json"]["opportunities"]
    assert all("evidence_status" in item for item in swot["result_json"]["opportunities"])

    marketing = client.post(f"/api/v1/startups/{startup['id']}/marketing-plan/runs").json()
    assert marketing["status"] == "ready"
    assert marketing["result_json"]["budget_guidance"]["amount_allocations"] is None
    assert marketing["result_json"]["kpis"][0]["target"] is None

    action_plan = client.post(f"/api/v1/startups/{startup['id']}/action-plans/runs").json()
    assert action_plan["status"] == "ready"
    assert action_plan["result_json"]["execution_enabled"] is False
    assert action_plan["result_json"]["budget"]["spend_authorized"] is False
