from app.schemas.research import MarketResearchRequest, MarketResearchResponse


class ResearchService:
    def generate_research(self, payload: MarketResearchRequest) -> MarketResearchResponse:
        return MarketResearchResponse(
            market_overview="Unknown: an approved Deep Search connector is required before market size or trend claims can be returned.",
            trends=[],
            competitors=[],
            opportunities=[],
            customer_pain_points=[],
            sources=[],
            numeric_claims=[],
            data_quality={
                "coverage": 0,
                "confidence": "low",
                "missing_fields": [
                    "verified_sources",
                    "market_estimates",
                    "competitor_evidence",
                    "customer_evidence",
                ],
                "conflicts": [],
                "assumptions": [
                    "No external research tool is configured for this compatibility endpoint.",
                    f"Requested scope: {payload.industry} in {payload.region} for {payload.audience_segment}.",
                ],
            },
        )


research_service = ResearchService()
