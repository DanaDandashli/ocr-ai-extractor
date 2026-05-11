"""
    Clean OCR/document extraction noise.
"""
def clean_text(text: str) -> str:
    lines = text.split("\n")
    cleaned = []

    for line in lines:
        line = line.strip()

        # Skip empty lines or very short noisy lines
        if not line or len(line) < 2:
            continue

        cleaned.append(line)

    return "\n".join(cleaned)


def normalize_currency(value: str) -> str:
    if not value:
        return "USD"
    
    mapping = {
        "$": "USD", "usd": "USD", "us$": "USD",
        "€": "EUR", "eur": "EUR", "euro": "EUR",
        "£": "GBP", "gbp": "GBP",
        "¥": "JPY", "jpy": "JPY", "yen": "JPY",
        "ll": "LBP", "lbp": "LBP", "l.l": "LBP", "leb": "LBP",
        "₹": "INR", "inr": "INR", "rs": "INR", "rs.": "INR",
        "aed": "AED", "dh": "AED", "dhs": "AED",
        "sar": "SAR", "sr": "SAR", "ريال": "SAR",
    }

    return mapping.get(value.strip().lower(), "USD")
