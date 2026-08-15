from pydantic import BaseModel, Field

from app.schemas.evidence import DataQuality, EvidenceSource, NumericClaim


class MarketResearchRequest(BaseModel):
    industry: str = Field(..., min_length=2)
    region: str = Field(..., min_length=2)
    audience_segment: str = Field(..., min_length=2)
    startup_id: int | None = Field(default=None, gt=0)


class Competitor(BaseModel):
    name: str
    strength: str | None = None
    weakness: str | None = None
    source_ids: list[str] = Field(default_factory=list)


class ResearchInsight(BaseModel):
    text: str
    source_ids: list[str] = Field(default_factory=list)
    confidence: str = "low"


class MarketResearchResponse(BaseModel):
    market_overview: str
    trends: list[ResearchInsight] = Field(default_factory=list)
    competitors: list[Competitor] = Field(default_factory=list)
    opportunities: list[ResearchInsight] = Field(default_factory=list)
    customer_pain_points: list[ResearchInsight] = Field(default_factory=list)
    sources: list[EvidenceSource] = Field(default_factory=list)
    numeric_claims: list[NumericClaim] = Field(default_factory=list)
    data_quality: DataQuality
