from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_search_service
from app.core.exceptions import ExternalSearchProviderError, RetrievalError
from app.models.search import SearchRequest, SearchResponse
from app.retrieval.service import SearchService


router = APIRouter()


@router.post("/search", response_model=SearchResponse, status_code=status.HTTP_200_OK)
def search(
    request: SearchRequest,
    service: SearchService = Depends(get_search_service),
) -> SearchResponse:
    try:
        return service.search(request)
    except ExternalSearchProviderError as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc)) from exc
    except RetrievalError as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)) from exc
