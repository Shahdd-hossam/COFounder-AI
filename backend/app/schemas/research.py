from pydantic import BaseModel, Field


class MarketResearchRequest(BaseModel):
    industry: str = Field(..., min_length=2)
    region: str = Field(..., min_length=2)
    audience_segment: str = Field(..., min_length=2)


class Competitor(BaseModel):
    name: str
    strength: str
    weakness: str


class MarketResearchResponse(BaseModel):
    trends: list[str]
    competitors: list[Competitor]
    opportunities: list[str]
    sources: list[dict] = Field(default_factory=list)
    numeric_claims: list[dict] = Field(default_factory=list)
    data_quality: dict = Field(default_factory=dict)
