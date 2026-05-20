import os, fitz, logging, re, json
from openai import APIConnectionError, RateLimitError, BadRequestError


def make_error(code, message, stage="input_validation", group="INPUT_ERROR"):
    return {"success": False, "stage": stage, "error_group": group, "error_code": code, "message": message}


def validate_input(file_path: str, ext: str):
    if not os.path.exists(file_path):
        return make_error("FILE_NOT_FOUND", "The file could not be found.")
    if os.path.getsize(file_path) == 0:
        return make_error("EMPTY_FILE", "The uploaded file is empty.")
    if ext == ".pdf":
        try:
            corrupted = fitz.open(file_path).page_count == 0
        except Exception:
            corrupted = True
        if corrupted:
            return make_error("CORRUPTED_PDF", "The PDF file is corrupted or has no readable pages.")
    return None


_INVALID_TYPES = {"blank", "empty", "blank sheet", "blank document", "blank_paper",
                  "blank page", "blank sheet of paper", "unknown", "none"}


def validate_output(result: dict) -> dict | None:
    if not isinstance(result, dict):
        return make_error("INVALID_RESULT_TYPE", "Internal error: invalid extraction result.", "final_validation")

    # Multi-page PDF result
    if result.get("pages"):
        for page in result["pages"]:
            error = validate_output(page)
            if error:
                return error
        return None

    # Multi-sheet Excel result
    if result.get("sheets"):
        for sheet in result["sheets"]:
            doc_type = str(sheet.get("document_type") or "").strip().lower()
            if doc_type and doc_type not in _INVALID_TYPES:
                return None  # at least one valid sheet → accept
        return make_error("NO_DOCUMENT_FOUND", "No valid document was detected.", "final_validation")

    # Single document
    # Accept if document has meaningful content even without document_type
    has_content = any(
        v not in (None, "", 0, 0.0, [], {})
        for k, v in result.items()
        if k != "document_type"
    )

    if not has_content and (not doc_type or doc_type in _INVALID_TYPES):
        return make_error(
            "NO_DOCUMENT_FOUND",
            "No valid document was detected. Please upload a clear document.",
            "final_validation"
        )
    
    return None


def handle_llm_exception(e: Exception) -> dict:
    if isinstance(e, RateLimitError):
        return make_error("RATE_LIMIT_EXCEEDED", "AI rate limit exceeded.", "system_error", "SYSTEM_ERROR")
    if isinstance(e, APIConnectionError):
        return make_error("API_CONNECTION_FAILED", "Could not connect to AI service.", "system_error", "SYSTEM_ERROR")
    if isinstance(e, BadRequestError):
        return make_error("INVALID_REQUEST", "AI service rejected the request.", "system_error", "SYSTEM_ERROR")
    logging.exception("Unexpected extraction error")
    return make_error("UNEXPECTED_SYSTEM_FAILURE", "Unexpected AI extraction failure.", "system_error", "SYSTEM_ERROR")


def safe_parse_json(raw: str) -> dict:
    if not raw or not isinstance(raw, str):
        return make_error("EMPTY_LLM_RESPONSE", "The AI returned an empty response.", "llm_error", "LLM_ERROR")

    cleaned = raw.strip()
    cleaned = re.sub(r"^```json\s*", "", cleaned)
    cleaned = re.sub(r"^```\s*",     "", cleaned)
    cleaned = re.sub(r"\s*```$",     "", cleaned)
    cleaned = cleaned.strip()

    # Attempt 1: direct parse
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    # Attempt 2: extract first {...} block
    try:
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if match:
            return json.loads(match.group())
    except json.JSONDecodeError:
        pass

    # Attempt 3: detect truncated JSON and report clearly
    if cleaned.startswith("{") and not cleaned.endswith("}"):
        return make_error(
            "TRUNCATED_JSON_RESPONSE",
            "The AI response was cut off. Try increasing _MAX_TOKENS in client.py.",
            "llm_error", "LLM_ERROR"
        )

    return make_error("INVALID_JSON_RESPONSE", "The AI returned malformed JSON.", "llm_error", "LLM_ERROR")
