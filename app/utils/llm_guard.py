import json
import re


# Step 1: Safe JSON Parsing
def safe_parse_json(raw_text: str):
    """
    Extracts and parses JSON even if LLM returns messy output.
    """

    if not raw_text or not isinstance(raw_text, str):
        return {
            "success": False,
            "stage": "llm",
            "error_code": "EMPTY_LLM_RESPONSE",
            "message": "The AI returned an empty response."
        }

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

    return {
        "success": False,
        "stage": "llm",
        "error_code": "INVALID_JSON_RESPONSE",
        "message": "The AI returned malformed JSON."
    }


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
        return {
            "success": False,
            "stage": "llm",
            "error_code": "SCHEMA_INVALID_TYPE",
            "message": "LLM output is not a valid object."
        }

    missing = [f for f in required_fields if f not in data]

    if missing:
        return {
            "success": False,
            "stage": "llm",
            "error_code": "SCHEMA_VALIDATION_FAILED",
            "message": f"Missing fields: {missing}"
        }

    return None


# Step 3: Normalization
def normalize_invoice(data: dict):
    """
    Ensures consistent types + safe defaults.
    """

    data["items"] = data.get("items") or []
    data["total"] = float(data.get("total") or 0.0)

    return data
