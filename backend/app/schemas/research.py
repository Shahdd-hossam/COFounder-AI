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
