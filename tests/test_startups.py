import os
import sys
from pathlib import Path

os.environ["DATABASE_URL"] = "sqlite:///./test_cofounder_ai.db"

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


def test_startup_create_read_and_revision() -> None:
    client = TestClient(app)
    payload = {
        "name": "CareerLaunch Egypt",
        "description": "An Arabic-English AI career coach for final-year university students.",
        "target_customer": "Final-year university students",
        "target_market": "Egypt, starting with Alexandria",
        "business_model": "Freemium subscription",
        "goal": "Acquire the first 100 qualified beta users",
        "budget": 10000,
        "currency": "EGP",
        "time_horizon_days": 30,
        "language": "Arabic and English",
    }

    created = client.post("/api/v1/startups", json=payload)
    assert created.status_code == 201
    startup = created.json()
    assert startup["context_revision"] == 1

    fetched = client.get(f"/api/v1/startups/{startup['id']}")
    assert fetched.status_code == 200
    assert fetched.json()["name"] == "CareerLaunch Egypt"

    changed = {**payload, "goal": "Acquire the first 200 qualified beta users"}
    updated = client.patch(f"/api/v1/startups/{startup['id']}", json=changed)
    assert updated.status_code == 200
    assert updated.json()["context_revision"] == 2


def test_health_and_readiness() -> None:
    client = TestClient(app)
    assert client.get("/health").json() == {"status": "ok"}
    assert client.get("/ready").json()["database"] == "connected"
