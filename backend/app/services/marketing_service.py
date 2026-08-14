from app.schemas.marketing import MarketingPlanRequest, MarketingPlanResponse
from app.services.ai_service import ai_service


class MarketingService:
    def generate_plan(self, payload: MarketingPlanRequest) -> MarketingPlanResponse:
        summary_prompt = (
            f"Create a concise go-to-market summary for {payload.company_name} "
            f"selling {payload.product} to {payload.target_audience} with goal: {payload.goal}."
        )

        summary = ai_service.build_summary(summary_prompt)
        channels = ["SEO + Content", "Paid Social", "Email Automation", "Partnerships"]
        budget_breakdown = {
            "Content": "30%",
            "Paid Media": "40%",
            "Lifecycle Marketing": "20%",
            "Experiments": "10%",
        }
        timeline = [
            "Week 1-2: Audience and positioning validation",
            "Week 3-4: Campaign setup and landing page optimization",
            "Week 5-8: Launch, learn, and iterate",
        ]

        return MarketingPlanResponse(
            summary=summary,
            channels=channels,
            budget_breakdown=budget_breakdown,
            timeline=timeline,
        )


marketing_service = MarketingService()
