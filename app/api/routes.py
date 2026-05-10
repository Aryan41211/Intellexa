from fastapi import APIRouter, HTTPException, Query, status

from app.api.schemas import ErrorResponse, HealthResponse, SearchResponse
from app.core.logger import get_logger
from app.retrieval.search import TavilySearch


router = APIRouter()
logger = get_logger(__name__)
search_client = TavilySearch()


@router.get(
    "/",
    response_model=HealthResponse,
    tags=["Health"],
    summary="Check API health",
)
def root() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse(message="AI Research Agent API is running.")


@router.get(
    "/search",
    response_model=SearchResponse,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse},
        status.HTTP_502_BAD_GATEWAY: {"model": ErrorResponse},
    },
    tags=["Search"],
    summary="Search the web with Tavily",
)
def search(query: str = Query(..., min_length=1, description="Web search query.")) -> SearchResponse:
    """Run a Tavily web search for the provided query."""
    try:
        results = search_client.search(query=query)
        return SearchResponse(query=query.strip(), count=len(results), results=results)
    except ValueError as exc:
        logger.warning("api.search.bad_request detail=%s", exc)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except RuntimeError as exc:
        logger.error("api.search.provider_error detail=%s", exc)
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc)) from exc
