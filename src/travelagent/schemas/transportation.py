from pydantic import BaseModel


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
