from agents import function_tool

from travelagent.tools._tavily_client import get_tavily_client, slim_results


@function_tool
def search_accommodation(
    destination: str,
    preference: str | None = None,
    max_results: int = 4,
) -> list[dict]:
    """Search for accommodation options in a destination.

    preference: optional hint such as a price level ("budget", "upscale"), type
    ("hostel", "apartment", "boutique"), or vibe ("central", "near beach", "quiet").
    Returns a list of raw web results, each with title, url, and content — extract the
    place's name, area, description, and tags from the content yourself.
    """
    query = (
        f"best {preference} places to stay in {destination}"
        if preference
        else f"best places to stay in {destination}"
    )
    response = get_tavily_client().search(query, max_results=max_results)
    return slim_results(response["results"])
