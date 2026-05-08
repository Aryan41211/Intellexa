# Autonomous Research Retrieval API

This repository contains the retrieval/search layer for an Autonomous Research
Agent Network. It exposes a small FastAPI service that accepts a query, calls
Tavily, and normalizes results into provider-neutral document objects.

## Architecture

The code is intentionally split by responsibility:

- `app/api/`: HTTP routes and FastAPI dependencies.
- `app/core/`: configuration, logging, and shared exceptions.
- `app/models/`: Pydantic request, response, and document contracts.
- `app/retrieval/`: provider interfaces, Tavily integration, and search service.
- `main.py`: local ASGI entrypoint.

Routes do not talk to Tavily directly. They call `SearchService`, which depends
on a `SearchProvider` interface. This keeps the API stable if future versions add
fallback providers, cached search, vector indexes, or provider-specific tuning.

## Setup

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Edit `.env` and set:

```bash
TAVILY_API_KEY=tvly-your-real-key
```

## Run Locally

```bash
uvicorn main:app --reload
```

Open the interactive API docs at:

```text
http://127.0.0.1:8000/docs
```

## Search Endpoint

`POST /search`

Example request:

```json
{
  "query": "What is retrieval augmented generation?",
  "max_results": 5,
  "search_depth": "advanced",
  "include_answer": true,
  "include_raw_content": false
}
```

Example response shape:

```json
{
  "query": "What is retrieval augmented generation?",
  "answer": "RAG combines retrieval with generation...",
  "response_time": 1.23,
  "results_count": 5,
  "documents": [
    {
      "title": "What is RAG?",
      "url": "https://example.com/rag",
      "content": "Retrieval augmented generation...",
      "metadata": {
        "source_provider": "tavily",
        "score": 0.91,
        "published_date": null,
        "raw": {
          "favicon": null,
          "images": []
        }
      }
    }
  ]
}
```

## Tests

```bash
pytest
```

The current unit test uses a fake provider so it verifies service behavior
without making network calls or consuming Tavily credits.
