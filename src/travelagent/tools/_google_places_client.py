import httpx

from travelagent.config import APP_CONFIG

_SEARCH_URL = "https://places.googleapis.com/v1/places:searchText"
_FIELD_MASK = "places.displayName,places.formattedAddress,places.regularOpeningHours.weekdayDescriptions,places.businessStatus"


def find_place(text_query: str) -> dict | None:
    """Look up a single place by free-text query (e.g. "Prado restaurant Lisbon").

    Returns the first match as a raw Places API result dict, or None if nothing matched.
    """
    if not APP_CONFIG.google_places_api_key:
        raise ValueError("GOOGLE_PLACES_API_KEY is not set in .env")

    response = httpx.post(
        _SEARCH_URL,
        json={"textQuery": text_query, "pageSize": 1},
        headers={
            "Content-Type": "application/json",
            "X-Goog-Api-Key": APP_CONFIG.google_places_api_key,
            "X-Goog-FieldMask": _FIELD_MASK,
        },
        timeout=10.0,
    )
    response.raise_for_status()
    places = response.json().get("places", [])
    return places[0] if places else None
