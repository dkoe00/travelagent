"""Pydantic schemas for transportation planning."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from travelagent.schemas.budget import TransportCostEstimate

TransportMode = Literal[
    "walking",
    "driving",
    "taxi",
    "rideshare",
    "public_transport",
]


class Geolocation(BaseModel):
    """Normalized geocoding candidate returned by the transportation tools."""

    display_name: str
    latitude: float
    longitude: float
    category: str | None = None
    kind: str | None = None
    importance: float | None = None


class GeolocationList(BaseModel):
    """Collection of normalized geocoding candidates for a query."""

    query: str
    locations: list[Geolocation]


class RouteEstimate(BaseModel):
    """Normalized route estimate between two geocoded locations."""

    origin_query: str
    destination_query: str
    origin: Geolocation
    destination: Geolocation
    mode: str
    distance_meters: float
    duration_seconds: float
    duration_minutes: float
    provider: str = "osrm"
    uncertainty_notes: list[str] = Field(default_factory=list)


class TransportOptionScore(BaseModel):
    """Comparable scores for one transportation option."""

    # TODO @dkoe00: Calibrate ranking weights.
    overall: float = Field(ge=0, le=1)
    time: float = Field(ge=0, le=1)
    cost: float = Field(ge=0, le=1)
    comfort: float = Field(ge=0, le=1)
    reliability: float = Field(ge=0, le=1)


class TransportOption(BaseModel):
    """One candidate way to travel between two places."""

    mode: TransportMode
    label: str
    route: RouteEstimate | None = None
    distance_meters: float = Field(ge=0)
    duration_minutes: float = Field(ge=0)
    comfort_score: float = Field(ge=0, le=1)
    reliability_score: float = Field(ge=0, le=1)
    cost_estimate: TransportCostEstimate | None = None
    score: TransportOptionScore | None = None
    ranking_reason: str
    pros: list[str] = Field(default_factory=list)
    cons: list[str] = Field(default_factory=list)
    uncertainty_notes: list[str] = Field(default_factory=list)
    include_for_strategic_decision: bool = False


class TransportRecommendation(BaseModel):
    """Ranked transportation options between an origin and destination."""

    origin_query: str
    destination_query: str
    origin: Geolocation
    destination: Geolocation
    recommended_option: TransportOption
    options: list[TransportOption]
    summary: str
    driving_option_included: bool
    uncertainty_notes: list[str] = Field(default_factory=list)
