from app.schemas.research import Competitor, MarketResearchRequest, MarketResearchResponse


class ResearchService:
    def generate_research(self, payload: MarketResearchRequest) -> MarketResearchResponse:
        trends = [
            f"Rising demand for specialized {payload.industry} offers in {payload.region}",
            "Higher CAC pressure is pushing brands toward retention-led growth",
            "Community-led brand trust is outperforming direct ad-only strategies",
        ]

        competitors = [
            Competitor(
                name="Competitor A",
                strength="Strong distribution partnerships",
                weakness="Weak niche differentiation",
            ),
            Competitor(
                name="Competitor B",
                strength="Aggressive performance marketing",
                weakness="Low organic loyalty",
            ),
        ]

        opportunities = [
            f"Target underserved {payload.audience_segment} audience with specialized messaging",
            "Use educational content funnels to lower acquisition costs",
            "Bundle services to increase average order value",
        ]

        return MarketResearchResponse(
            trends=trends,
            competitors=competitors,
            opportunities=opportunities,
        )


research_service = ResearchService()
