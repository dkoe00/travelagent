from pydantic import BaseModel


class DestinationSuggestion(BaseModel):
    name: str           # e.g. "Albanian Riviera"
    country: str        # e.g. "Albania"
    why: str            # 1-2 sentences on why it matches the user's constraints
    tags: list[str]     # e.g. ["coastal hiking", "budget", "off the beaten path", "May–Sep"]


class DestinationList(BaseModel):
    suggestions: list[DestinationSuggestion]
