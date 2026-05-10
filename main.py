from fastapi import FastAPI

from app.api.routes import router
from app.core.config import settings
from app.core.logger import configure_logging

configure_logging(settings.LOG_LEVEL)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Compact FastAPI backend for web retrieval and AI research workflows.",
    contact={"name": "AI Research Agent"},
    openapi_tags=[
        {"name": "Health", "description": "Basic service status endpoints."},
        {"name": "Search", "description": "Tavily-powered web retrieval endpoints."},
    ],
)
app.include_router(router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
