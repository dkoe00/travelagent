from pydantic import BaseModel


class ItineraryStop(BaseModel):
    time_of_day: str    # "morning" | "lunch" | "afternoon" | "evening"
    place_name: str     # a place from the pool, or a generic filler like "free time"
    note: str           # 1 short sentence: what to do there / why this slot


class ItineraryDay(BaseModel):
    day: int            # 1-based
    theme: str          # short label, e.g. "Old Town & viewpoints"
    stops: list[ItineraryStop]


class Itinerary(BaseModel):
    destination: str
    days: list[ItineraryDay]
