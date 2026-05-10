from pydantic import BaseModel, Field, HttpUrl


class HealthResponse(BaseModel):
    message: str


class ErrorResponse(BaseModel):
    detail: str


class SearchResult(BaseModel):
    title: str = Field(default="", description="Result title from Tavily.")
    url: HttpUrl = Field(description="Canonical URL for the result.")
    content: str = Field(default="", description="Short content snippet or summary.")


class SearchResponse(BaseModel):
    query: str
    count: int
    results: list[SearchResult]
