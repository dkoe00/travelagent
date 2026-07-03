from tavily import TavilyClient

from travelagent.config import APP_CONFIG

_client: TavilyClient | None = None


def get_tavily_client() -> TavilyClient:
    global _client
    if _client is None:
        if not APP_CONFIG.tavily_api_key:
            raise ValueError("TAVILY_API_KEY is not set in .env")
        _client = TavilyClient(api_key=APP_CONFIG.tavily_api_key)
    return _client


def slim_results(results: list[dict], max_content_chars: int = 800) -> list[dict]:
    """Reduce raw Tavily results to the fields the agents actually read.

    Full payloads (relevance scores, kilobytes of page text per result) inflate the
    agent's next LLM request; the large synthesis request was observed to fail with
    connection errors on the proxy endpoint.
    """
    return [
        {
            "title": r.get("title"),
            "url": r.get("url"),
            "content": (r.get("content") or "")[:max_content_chars],
        }
        for r in results
    ]
