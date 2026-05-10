import re


_CONTROL_CHARS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
_HORIZONTAL_SPACE = re.compile(r"[ \t\r\f\v]+")
_EXCESSIVE_NEWLINES = re.compile(r"\n{3,}")


def clean_text(text: str) -> str:
    """Normalize extracted text for retrieval, embeddings, and agent context."""
    if not text:
        return ""

    cleaned = text.replace("\xa0", " ").replace("\r", " ")
    cleaned = _CONTROL_CHARS.sub("", cleaned)
    cleaned = "\n".join(_HORIZONTAL_SPACE.sub(" ", line).strip() for line in cleaned.splitlines())
    cleaned = _EXCESSIVE_NEWLINES.sub("\n\n", cleaned)

    return cleaned.strip()
