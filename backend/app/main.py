from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import market_research, marketing_plan, swot
from app.core.config import get_settings

settings = get_settings()
app = FastAPI(title=settings.app_name, version=settings.app_version, debug=settings.debug)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(marketing_plan.router, prefix=settings.api_prefix)
app.include_router(market_research.router, prefix=settings.api_prefix)
app.include_router(swot.router, prefix=settings.api_prefix)
