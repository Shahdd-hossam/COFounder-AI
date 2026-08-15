from app.schemas.research import Competitor, MarketResearchRequest, MarketResearchResponse


class ResearchService:
    def generate_research(self, payload: MarketResearchRequest) -> MarketResearchResponse:
        return MarketResearchResponse(
            trends=[f"Research tool not connected for {payload.industry} in {payload.region}."],
            competitors=[],
            opportunities=[f"Collect verified evidence for {payload.audience_segment}."],
            sources=[],
            numeric_claims=[],
            data_quality={
                "confidence": "low",
                "missing_fields": ["verified_sources", "market_estimates"],
                "assumptions": ["This compatibility endpoint does not claim external research."],
            },
        )


research_service = ResearchService()
