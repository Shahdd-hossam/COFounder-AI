from app.schemas.swot import SWOTRequest, SWOTResponse


class SWOTService:
    def generate_swot(self, payload: SWOTRequest) -> SWOTResponse:
        strengths = [
            f"Clear value proposition around {payload.product}",
            "Fast decision-making due to lean team structure",
            "Strong founder-market fit",
        ]
        weaknesses = [
            "Limited marketing budget compared to larger competitors",
            "Low brand awareness in new segments",
            "Dependence on a narrow acquisition channel mix",
        ]
        opportunities = [
            f"Expand with localized campaigns in {payload.market_context}",
            "Use influencer collaborations to accelerate trust",
            "Differentiate with outcome-based pricing models",
        ]
        threats = [
            "Ad platform volatility and rising CPM",
            "New entrants with discounted pricing",
            "Economic pressure reducing discretionary spend",
        ]

        return SWOTResponse(
            strengths=strengths,
            weaknesses=weaknesses,
            opportunities=opportunities,
            threats=threats,
        )


swot_service = SWOTService()
