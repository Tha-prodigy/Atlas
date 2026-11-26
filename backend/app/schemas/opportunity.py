from datetime import datetime

from pydantic import BaseModel, ConfigDict


class OpportunityResponse(BaseModel):
    id: int
    title: str
    slug: str
    summary: str
    problem: str
    proposed_solution: str
    target_market: str | None
    revenue_model: str | None
    operational_requirements: str | None
    risks: str | None
    country_id: int
    business_model_id: int
    status: str
    is_featured: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)