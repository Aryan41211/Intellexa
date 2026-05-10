from typing import TypedDict
from urllib.parse import urlparse

import requests
import trafilatura

from app.core.config import settings
from app.core.logger import get_logger
from app.retrieval.cleaner import clean_text


logger = get_logger(__name__)


class ExtractedDocument(TypedDict):
    title: str
    url: str
    content: str


def is_valid_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def extract_document(url: str, title: str = "") -> ExtractedDocument | None:
    """Download a URL and extract readable article text."""
    if not is_valid_url(url):
        logger.warning("extract.invalid_url url=%r", url)
        return None

    try:
        logger.info("extract.request url=%r", url)
        response = requests.get(
            url,
            timeout=settings.EXTRACTION_TIMEOUT_SECONDS,
            headers={"User-Agent": f"{settings.APP_NAME}/{settings.APP_VERSION}"},
        )
        response.raise_for_status()
    except requests.Timeout:
        logger.warning("extract.timeout url=%r", url)
        return None
    except requests.RequestException as exc:
        logger.warning("extract.download_failed url=%r error=%s", url, exc)
        return None

    try:
        extracted_text = trafilatura.extract(
            response.text,
            url=url,
            include_comments=False,
            include_tables=False,
            no_fallback=False,
        )
    except Exception as exc:
        logger.warning("extract.parse_failed url=%r error=%s", url, exc)
        return None
    content = clean_text(extracted_text or "")

    if not content:
        logger.warning("extract.empty_content url=%r", url)
        return None

    logger.info("extract.success url=%r chars=%s", url, len(content))
    return {"title": title.strip(), "url": url, "content": content}
