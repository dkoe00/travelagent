from pydantic import BaseModel


class Place(BaseModel):
    kind: str           # "activity" | "restaurant" | "cafe" | "accommodation"
    name: str
    area: str
    description: str
    tags: list[str]     # carries cuisine, price, notability, vibe — e.g. ["italian", "budget", "hidden gem"]


class PlacesPool(BaseModel):
    destination: str
    places: list[Place]
