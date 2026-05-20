import os
from dateutil import parser as dateparser
from app.lookup import CURRENCY_MAP


# It strips noise from the raw extracted text - empty lines, extra whitespace - before sending it to the LLM
def clean_text(text: str) -> str:
    return "\n".join(line.strip() for line in text.splitlines() if line.strip())


def remove_none_fields(data):
    """Recursively remove keys with None values from dicts and lists."""
    if isinstance(data, dict):
        return {
            k: remove_none_fields(v)
            for k, v in data.items()
            if v is not None and v != 0.0 and v != ""
        }
    if isinstance(data, list):
        return [remove_none_fields(i) for i in data]
    return data


def cleanup_images(image_paths: list):
    """Remove temporary page images after extraction."""
    for path in image_paths:
        try:
            if os.path.exists(path):
                os.remove(path)
        except OSError as e:
            print(f"[WARN] Could not delete temp file {path}: {e}")


def normalize_date(value: str) -> str | None:
    try:
        return dateparser.parse(value).strftime("%Y-%m-%d")
    except Exception:
        return value


def normalize_currency(value: str) -> str:
    """Map currency symbol/alias to ISO 4217 code. Defaults to 'USD'."""
    if not value:
        return "USD"
    return CURRENCY_MAP.get(value.strip().lower(), value.strip().upper())
