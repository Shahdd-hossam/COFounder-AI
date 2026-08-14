from fastapi import APIRouter

from app.schemas.swot import SWOTRequest, SWOTResponse
from app.services.swot_service import swot_service

router = APIRouter(prefix="/swot", tags=["SWOT"])


@router.post("", response_model=SWOTResponse)
def build_swot(payload: SWOTRequest) -> SWOTResponse:
    return swot_service.generate_swot(payload)
