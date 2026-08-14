from fastapi import APIRouter

from app.schemas.marketing import MarketingPlanRequest, MarketingPlanResponse
from app.services.marketing_service import marketing_service

router = APIRouter(prefix="/marketing-plan", tags=["Marketing Plan"])


@router.post("", response_model=MarketingPlanResponse)
def create_marketing_plan(payload: MarketingPlanRequest) -> MarketingPlanResponse:
    return marketing_service.generate_plan(payload)
