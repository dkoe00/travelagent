from agents import function_tool

from travelagent.tools._tavily_client import get_tavily_client, slim_results


@function_tool
def search_restaurants(
    destination: str,
    preference: str | None = None,
    max_results: int = 6,
) -> list[dict]:
    """Search for restaurants and cafes in a destination.

    preference: optional free-text hint such as a cuisine type ("italian", "seafood"),
    price level ("budget", "upscale"), or vibe ("hidden gem", "special occasion").
    Returns a list of raw web results, each with title, url, and content — extract the
    place's name, area, description, and tags from the content yourself.
    """
    query = (
        f"best {preference} restaurants in {destination}"
        if preference
        else f"best restaurants and cafes in {destination}"
    )
    response = get_tavily_client().search(query, max_results=max_results)
    return slim_results(response["results"])
