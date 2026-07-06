from pydantic import BaseModel


class ItineraryStop(BaseModel):
    time_of_day: str    # "morning" | "lunch" | "afternoon" | "evening"
    place_name: str     # a place from the pool, or a generic filler like "free time"
    note: str           # 1 short sentence: what to do there / why this slot
    transport_note: str | None = None  # optional route or transfer note for reaching this stop


class ItineraryDay(BaseModel):
    day: int            # 1-based
    theme: str          # short label, e.g. "Old Town & viewpoints"
    stops: list[ItineraryStop]
    mobility_note: str | None = None  # optional day-level walking/transfer/area-clustering note


class Itinerary(BaseModel):
    destination: str
    days: list[ItineraryDay]
    transport_summary: str | None = None
