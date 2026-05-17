# ── Currency mapping ──────────────────────────────────────────────────────────
CURRENCY_MAP = {
    "$": "USD", "usd": "USD", "us$": "USD",
    "€": "EUR", "eur": "EUR", "euro": "EUR",
    "£": "GBP", "gbp": "GBP",
    "¥": "JPY", "jpy": "JPY", "yen": "JPY",
    "₺": "TRY", "try": "TRY", "turkish lira": "TRY",
    "₹": "INR", "inr": "INR", "rs": "INR",
    "aed": "AED", "dh": "AED", "dhs": "AED",
    "sar": "SAR", "sr": "SAR",
    "ll": "LBP", "lbp": "LBP",
}

# ── Supported file extensions ─────────────────────────────────────────────────
SUPPORTED_EXTENSIONS = {
    ".pdf":  "pdf",
    ".png":  "image",
    ".jpg":  "image",
    ".jpeg": "image",
    ".webp": "image",
    ".docx": "text",
    ".xlsx": "text",
    ".xls":  "text",
    ".html": "text",
    ".htm":  "text",
    ".txt":  "text",
    ".xml":  "text",
    ".eml":  "text",
}

# ── Document type labels ──────────────────────────────────────────────────────
DOCUMENT_TYPES = [
    "invoice",
    "receipt",
    "contract",
    "report",
    "form",
    "letter",
    "purchase_order",
    "delivery_note",
    "other",
]

# ── Lookup functions ──────────────────────────────────────────────────────────


def normalize_currency(value: str) -> str:
    """Map currency symbol/alias to ISO 4217 code. Defaults to 'USD'."""
    if not value:
        return "USD"
    return CURRENCY_MAP.get(value.strip().lower(), value.strip().upper())


def get_file_type(extension: str) -> str | None:
    """Return pipeline type for a given file extension, or None if unsupported."""
    return SUPPORTED_EXTENSIONS.get(extension.strip().lower())


def is_supported(extension: str) -> bool:
    """Check if a file extension is supported."""
    return extension.strip().lower() in SUPPORTED_EXTENSIONS
