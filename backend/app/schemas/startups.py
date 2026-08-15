from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class StartupCreate(BaseModel):
    name: str = Field(min_length=2, max_length=160)
    description: str = Field(min_length=10)
    target_customer: str = Field(min_length=2)
    target_market: str = Field(min_length=2)
    business_model: str = Field(min_length=2, max_length=200)
    goal: str = Field(min_length=3)
    budget: Decimal = Field(gt=0)
    currency: str = Field(min_length=3, max_length=8)
    time_horizon_days: int = Field(gt=0, le=3650)
    language: str = Field(min_length=2, max_length=80)


class StartupUpdate(StartupCreate):
    pass


class StartupResponse(StartupCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    context_revision: int
    created_at: datetime
    updated_at: datetime


class WorkflowRunResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    startup_id: int
    feature: str
    status: str
    stage: str | None
    progress_percent: int
    tool_name: str | None
    context_revision: int
    input_revisions_json: dict
    result_json: dict | None
    error_code: str | None
    error_message: str | None
    started_at: datetime | None
    completed_at: datetime | None
    created_at: datetime
