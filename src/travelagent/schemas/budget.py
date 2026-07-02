"""Pydantic schemas for budget estimates."""

from __future__ import annotations

from pydantic import BaseModel, Field


class MoneyEstimate(BaseModel):
    """Estimated monetary amount in a single currency."""

    amount: float = Field(ge=0)
    currency: str = Field(min_length=3, max_length=3)


class CostRange(BaseModel):
    """Estimated lower and upper bound in a single currency."""

    min: MoneyEstimate
    max: MoneyEstimate


class TransportCostEstimate(BaseModel):
    """Cost estimate for one transportation option."""

    mode: str
    distance_meters: float = Field(ge=0)
    duration_minutes: float = Field(ge=0)
    estimated_cost: MoneyEstimate
    estimated_range: CostRange | None = None
    confidence: str = "medium"
    assumptions: list[str] = Field(default_factory=list)
