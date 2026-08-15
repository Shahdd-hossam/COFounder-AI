import os
import sys
from pathlib import Path

os.environ["DATABASE_URL"] = "sqlite:///./test_mock_profiles.db"

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


def create(client: TestClient, description: str, market: str) -> dict:
    return client.post("/api/v1/startups", json={
        "name": "Any Name",
        "description": description,
        "target_customer": "Primary customers",
        "target_market": market,
        "business_model": "Subscription",
        "goal": "Validate demand",
        "budget": 5000,
        "currency": "USD",
        "time_horizon_days": 30,
        "language": "English",
    }).json()


def test_description_similarity_returns_coherent_career_profile() -> None:
    client = TestClient(app)
    startup = create(client, "Bilingual AI career coach for university students preparing resumes and interviews", "Egypt")
    result = client.post(f"/api/v1/startups/{startup['id']}/market-research/runs").json()["result_json"]
    assert result["mock_profile_key"] == "career_coach_egypt"
    assert len(result["sources"]) >= 2
    assert len(result["competitors"]) >= 3
    assert result["similarity"]["matched_keywords"]


def test_description_similarity_returns_nonempty_generic_profile() -> None:
    client = TestClient(app)
    startup = create(client, "A workflow automation dashboard for small business operations teams", "United States")
    result = client.post(f"/api/v1/startups/{startup['id']}/market-research/runs").json()["result_json"]
    assert result["mock_profile_key"] in {"b2b_saas", "generic_startup"}
    assert result["sources"]
    assert result["competitors"]
    assert result["market_overview"]
