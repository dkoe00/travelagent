from pydantic import BaseModel, Field


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
