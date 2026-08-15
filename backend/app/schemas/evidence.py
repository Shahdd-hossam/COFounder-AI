from datetime import date
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field, HttpUrl


NumberType = Literal["source_reported", "derived_from_sources", "modeled_estimate", "unknown"]


class EvidenceSource(BaseModel):
    title: str
    publisher: str | None = None
    url: HttpUrl | None = None
    retrieved_on: date | None = None
    quality: Literal["low", "medium", "high"] = "medium"


class NumericClaim(BaseModel):
    label: str
    value: Decimal | None = None
    unit: str | None = None
    currency: str | None = None
    geography: str | None = None
    period: str | None = None
    number_type: NumberType
    source_ids: list[str] = Field(default_factory=list)
    methodology: str | None = None
    confidence: Literal["low", "medium", "high"] = "low"
    assumptions: list[str] = Field(default_factory=list)


class DataQuality(BaseModel):
    coverage: float = Field(ge=0, le=1)
    confidence: Literal["low", "medium", "high"]
    missing_fields: list[str] = Field(default_factory=list)
    conflicts: list[str] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
