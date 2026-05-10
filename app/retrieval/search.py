from tavily import TavilyClient

from app.core.config import settings
from app.core.logger import get_logger
from app.retrieval.cleaner import clean_text
from app.retrieval.extractor import extract_document


logger = get_logger(__name__)


class TavilySearch:
    """Small wrapper around Tavily search operations."""

    def __init__(self) -> None:
        settings.validate_required_secrets()
        self.client = TavilyClient(api_key=settings.TAVILY_API_KEY)

    def search(self, query: str, max_results: int | None = None) -> list[dict[str, str]]:
        """Search the web, extract pages, and return clean retrieval documents."""
        cleaned_query = query.strip() if query else ""
        result_limit = max_results or settings.DEFAULT_SEARCH_RESULTS

        if not cleaned_query:
            raise ValueError("Search query cannot be empty.")

        try:
            logger.info("search.request query=%r max_results=%s", cleaned_query, result_limit)
            response = self.client.search(
                query=cleaned_query,
                search_depth=settings.TAVILY_SEARCH_DEPTH,
                max_results=result_limit,
            )
        except Exception as exc:
            logger.exception("search.failure query=%r", cleaned_query)
            raise RuntimeError("Tavily search request failed.") from exc

        results = response.get("results", [])
        documents: list[dict[str, str]] = []

        for item in results:
            url = item.get("url", "")
            title = item.get("title", "")
            snippet = clean_text(item.get("content", ""))

            if not url:
                logger.warning("search.result_missing_url query=%r title=%r", cleaned_query, title)
                continue

            document = extract_document(url=url, title=title)
            if document:
                documents.append(document)
                continue

            if snippet:
                logger.info("search.fallback_snippet url=%r", url)
                documents.append({"title": title, "url": url, "content": snippet})

        logger.info(
            "search.success query=%r result_count=%s",
            cleaned_query,
            len(documents),
        )
        return documents
