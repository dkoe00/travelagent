from agents import function_tool

from travelagent.tools._tavily_client import get_tavily_client, slim_results


@function_tool
def web_search(query: str, max_results: int = 5) -> list[dict]:
    """Search the web for up-to-date travel information.

    Use this to find current details about a destination, activity, or travel topic —
    for example opening hours, seasonal tips, trail conditions, local events, or
    recent traveller reports.
    Returns a list of raw web results, each with title, url, and content.
    """
    response = get_tavily_client().search(query, max_results=max_results)
    return slim_results(response["results"])
