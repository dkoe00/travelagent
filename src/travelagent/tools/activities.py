from agents import function_tool

from travelagent.tools._tavily_client import get_tavily_client, slim_results

_CATEGORY_QUERIES: dict[str, str] = {
    "museum": "best museums to visit in {destination}",
    "historic": "historic sites and landmarks in {destination}",
    "viewpoint": "best viewpoints and scenic spots in {destination}",
    "park": "parks and gardens in {destination}",
    "hiking": "best hiking trails near {destination}",
    "beach": "best beaches in {destination}",
    "market": "local markets in {destination}",
    "gallery": "art galleries in {destination}",
}
_FALLBACK_QUERY = "top things to do in {destination}"


@function_tool
def search_activities(destination: str, category: str, max_results: int = 5) -> list[dict]:
    """Search for activities and points of interest in a destination by category.

    Categories: museum, historic, viewpoint, park, hiking, beach, market, gallery.
    Returns a list of raw web results, each with title, url, and content — extract the
    place's name, area, description, and tags from the content yourself.
    """
    query_template = _CATEGORY_QUERIES.get(category.lower(), _FALLBACK_QUERY)
    query = query_template.format(destination=destination)
    response = get_tavily_client().search(query, max_results=max_results)
    return slim_results(response["results"])
