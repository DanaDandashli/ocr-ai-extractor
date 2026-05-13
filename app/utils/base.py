import json
from llm.cleaner import normalize_currency
from .llm_guard import safe_parse_json, validate_schema,normalize_invoice


def parse_json_response(result: str) -> dict:

    # Step 1: Safe JSON Parsing (handles broken JSON)
    data = safe_parse_json(result)

    # If parsing failed -> return immediately
    if isinstance(data, dict) and data.get("success") is False:
        return data
    
    # Step 2: Schema Validation
    error = validate_schema(data)
    if error:
        return error

    # Step 3: Normalization
    data = normalize_invoice(data)

    # Step 4: currency normalization
    data["currency"] = normalize_currency(data.get("currency"))
    
    return data
