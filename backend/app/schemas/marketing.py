from pydantic import BaseModel, Field


class MarketingPlanRequest(BaseModel):
    company_name: str = Field(..., min_length=2)
    product: str = Field(..., min_length=2)
    target_audience: str = Field(..., min_length=2)
    goal: str = Field(..., min_length=3)


class MarketingPlanResponse(BaseModel):
    summary: str
    channels: list[str]
    budget_breakdown: dict[str, str]
    timeline: list[str]
    data_quality: dict = Field(default_factory=dict)
