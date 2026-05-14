import json, re
from utils.handle_errors import make_error


# Step 1: Safe JSON Parsing
def safe_parse_json(raw_text: str):
    """
    Extracts and parses JSON even if LLM returns messy output.
    """

    if not raw_text or not isinstance(raw_text, str):
        return make_error(
            "EMPTY_LLM_RESPONSE",
            "The AI returned an empty response.",
            "llm_error",
            "LLM_ERROR"
        )

    try:
        # Try direct parsing first
        return json.loads(raw_text)

    except Exception:
        pass

    # Try extracting JSON block
    try:
        json_match = re.search(r"\{.*\}", raw_text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
    except Exception:
        pass

    return make_error(
        "INVALID_JSON_RESPONSE",
        "The AI returned malformed JSON.",
        "llm_error",
        "LLM_ERROR"
    )


# Step 2: Schema Validation
def validate_schema(data: dict):
    """
    Ensures required invoice structure exists.
    """

    required_fields = [
        "invoice_number",
        "date",
        "vendor_name",
        "customer_name",
        "items",
        "total",
        "currency"
    ]

    if not isinstance(data, dict):
        return make_error(
            "SCHEMA_INVALID_TYPE",
            "LLM output is not a valid object.",
            "llm_error",
            "LLM_ERROR"
        )

    missing = [f for f in required_fields if f not in data]

    if missing:
        return make_error(
            "SCHEMA_VALIDATION_FAILED",
            f"Missing fields: {missing}",
            "llm_error",
            "LLM_ERROR"
        )
    
    return None


# Step 3: Normalization
def normalize_invoice(data: dict):
    """
    Ensures consistent types + safe defaults.
    """

    data["items"] = data.get("items") or []
    data["total"] = float(data.get("total") or 0.0)

    return data
