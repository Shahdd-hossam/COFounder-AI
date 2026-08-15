from app.schemas.swot import SWOTRequest, SWOTResponse


class SWOTService:
    def generate_swot(self, payload: SWOTRequest) -> SWOTResponse:
        return SWOTResponse(
            strengths=[f"The product has a defined focus on {payload.product}."],
            weaknesses=["Verified market research is not connected to this compatibility endpoint."],
            opportunities=[f"Validate demand in {payload.market_context}."],
            threats=["Competitor and channel risks require source-backed research."],
            provenance=[
                {"basis": "request_context", "confidence": "low"},
                {"basis": "missing_research", "confidence": "low"},
            ],
        )


swot_service = SWOTService()
