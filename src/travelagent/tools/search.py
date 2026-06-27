from agents import function_tool

_MOCK_RESULTS: list[dict] = [
    {
        "title": "Top things to do in Lisbon — travel guide",
        "url": "https://example.com/lisbon-guide",
        "snippet": "Lisbon's Alfama neighbourhood is home to the oldest Fado houses in the city. The Castelo de São Jorge offers panoramic views. Don't miss the pastéis de nata at the original Pastéis de Belém.",
    },
    {
        "title": "Coastal hiking trails in Portugal — routes and tips",
        "url": "https://example.com/portugal-coastal-hikes",
        "snippet": "The Fishermen's Trail (Rota Vicentina) runs 120 km along the Alentejo coast — one of Europe's wildest and least-developed coastlines. Best hiked April–June before summer heat.",
    },
    {
        "title": "Best time to visit Albania — travel advice",
        "url": "https://example.com/albania-travel",
        "snippet": "May to September is peak season. The Albanian Riviera sees temperatures of 28–32°C in July and August. The Accursed Mountains are best visited June–September for hiking.",
    },
]


@function_tool
def web_search(query: str, max_results: int = 5) -> list[dict]:
    """Search the web for up-to-date travel information.

    Use this to find current details about a destination, activity, or travel topic —
    for example opening hours, seasonal tips, trail conditions, local events, or
    recent traveller reports.
    Returns a list of results with title, url, and a short snippet.
    """
    return _MOCK_RESULTS[:max_results]  # MOCK — replace with: TavilyClient().search(query, max_results=max_results)
