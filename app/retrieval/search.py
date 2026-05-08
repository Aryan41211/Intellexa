from tavily import TavilyClient

from app.core.config import settings


class TavilySearch:
    """Small wrapper around Tavily search operations."""

    def __init__(self) -> None:
        settings.validate()
        self.client = TavilyClient(api_key=settings.TAVILY_API_KEY)

    def search(self, query: str, max_results: int = 5) -> list[dict[str, str]]:
        """Search the web and return only the fields the API should expose."""
        if not query or not query.strip():
            raise ValueError("Search query cannot be empty.")

        try:
            response = self.client.search(
                query=query.strip(),
                search_depth="advanced",
                max_results=max_results,
            )
        except Exception as exc:
            # Keep Tavily-specific errors behind a clean application error.
            raise RuntimeError("Tavily search request failed.") from exc

        results = response.get("results", [])
        return [
            {
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "content": item.get("content", ""),
            }
            for item in results
        ]
