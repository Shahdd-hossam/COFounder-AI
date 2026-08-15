from pydantic import BaseModel, Field


class SWOTRequest(BaseModel):
    company_name: str = Field(..., min_length=2)
    product: str = Field(..., min_length=2)
    market_context: str = Field(..., min_length=2)


class SWOTResponse(BaseModel):
    strengths: list[str]
    weaknesses: list[str]
    opportunities: list[str]
    threats: list[str]
    provenance: list[dict] = Field(default_factory=list)
