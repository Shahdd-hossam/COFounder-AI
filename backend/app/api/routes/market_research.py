from fastapi import APIRouter

from app.schemas.research import MarketResearchRequest, MarketResearchResponse
from app.services.research_service import research_service

router = APIRouter(prefix="/market-research", tags=["Market Research"])


@router.post("", response_model=MarketResearchResponse)
def run_market_research(payload: MarketResearchRequest) -> MarketResearchResponse:
    return research_service.generate_research(payload)
