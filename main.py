from fastapi import FastAPI, HTTPException, Query

from app.retrieval.search import TavilySearch

app = FastAPI(title="AI Research Agent")
search_client = TavilySearch()


@app.get("/")
def root() -> dict[str, str]:
    """Health check endpoint."""
    return {"message": "AI Research Agent API is running."}


@app.get("/search")
def search(query: str = Query(..., min_length=1)) -> dict[str, list[dict[str, str]]]:
    """Run a Tavily web search for the provided query."""
    try:
        results = search_client.search(query=query)
        return {"results": results}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
