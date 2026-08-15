from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError

from app.api.routes import market_research, marketing_plan, startups, swot, workflows
from app.core.config import get_settings
from app.db.models import Base
from app.db.session import check_database, get_engine, get_session_factory
from app.services.mock_research_service import seed_mock_profiles

settings = get_settings()
app = FastAPI(title=settings.app_name, version=settings.app_version, debug=settings.debug)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def initialize_local_database() -> None:
    # This creates tables for the local SQLite fallback. Manus production should
    # use reviewed migrations instead of relying on application startup DDL.
    if settings.database_url.startswith("sqlite"):
        Base.metadata.create_all(bind=get_engine(settings))
    try:
        with get_session_factory(settings)() as db:
            if settings.mock_profiles_enabled:
                seed_mock_profiles(db)
            db.commit()
    except SQLAlchemyError:
        # A migration must create the table in Manus production before seeding.
        pass


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/ready")
def readiness() -> dict[str, str]:
    try:
        check_database(settings)
        database_status = "connected"
        overall = "ready"
    except (RuntimeError, SQLAlchemyError) as exc:
        database_status = "not_configured" if isinstance(exc, RuntimeError) else "error"
        overall = "degraded"

    return {
        "status": overall,
        "database": database_status,
        "mcp": "configured" if settings.mcp_enabled else "not_configured",
        "mock_profiles": "seeded",
        "llm": "configured" if (settings.llm_enabled and (settings.llm_api_key or settings.manus_enabled)) else "not_configured",
    }


app.include_router(startups.router, prefix=settings.api_prefix)
app.include_router(startups.workflow_router, prefix=settings.api_prefix)
app.include_router(workflows.router, prefix=settings.api_prefix)
app.include_router(marketing_plan.router, prefix=settings.api_prefix)
app.include_router(market_research.router, prefix=settings.api_prefix)
app.include_router(swot.router, prefix=settings.api_prefix)
