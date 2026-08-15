from app.schemas.marketing import MarketingPlanRequest, MarketingPlanResponse


class MarketingService:
    def generate_plan(self, payload: MarketingPlanRequest) -> MarketingPlanResponse:
        return MarketingPlanResponse(
            summary=(
                f"A verified strategy for {payload.company_name} requires the shared startup "
                "context and approved strategy tool."
            ),
            channels=[],
            budget_breakdown={},
            timeline=[],
            data_quality={
                "confidence": "low",
                "missing_fields": ["startup_context", "research", "strategy_tool"],
                "assumptions": ["No unsupported channel or budget recommendation was invented."],
            },
        )


marketing_service = MarketingService()
