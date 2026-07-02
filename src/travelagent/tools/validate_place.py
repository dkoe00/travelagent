from agents import function_tool

from travelagent.tools._google_places_client import find_place


@function_tool
def validate_place(name: str, destination: str) -> dict:
    """Validate that a candidate place actually exists and fetch its address and opening hours.

    Call this once per candidate place you extracted from search results, to enrich it
    with real-world data. If the place cannot be found, `found` is False — keep the place
    in the pool anyway, just without address/opening_hours (validation enriches, it never
    filters out a place).
    """
    match = find_place(f"{name}, {destination}")
    if match is None:
        return {"found": False, "address": None, "opening_hours": None}

    return {
        "found": True,
        "address": match.get("formattedAddress"),
        "opening_hours": match.get("regularOpeningHours", {}).get("weekdayDescriptions"),
    }
