import os, fitz, logging 
from openai import APIConnectionError, RateLimitError, BadRequestError


def make_error(code, message, stage="input_validation", group="INPUT_ERROR"):
    return {
        "success": False,
        "stage": stage,
        "error_group": group,
        "error_code": code,
        "message": message
    }


def input_file_validation(file_path: str, ext: str):
    """
    Detects empty or corrupted files before processing.
    Returns structured error OR None if valid.
    """

    # if file not found
    if not os.path.exists(file_path):
        return make_error(
            "FILE_NOT_FOUND",
            "The file could not be found. Please check the path and try again."
        )

    # Empty file check
    if os.path.getsize(file_path) == 0:
        return make_error(
            "EMPTY_FILE",
            "The uploaded file is empty. Please upload a valid document."
        )

    # PDF corruption check
    if ext == ".pdf":
        try:
            doc = fitz.open(file_path)
            if doc.page_count == 0:
                return make_error(
                    "CORRUPTED_PDF",
                    "The PDF file appears corrupted or has no readable pages."
                )

        except Exception:
            return make_error(
                "CORRUPTED_PDF",
                "The PDF file is corrupted or cannot be opened."
            )

    return None


def handle_llm_exception(e: Exception) -> dict:
    if isinstance(e, RateLimitError):
        return make_error("RATE_LIMIT_EXCEEDED", "AI rate limit exceeded.", "system_error", "SYSTEM_ERROR")
    if isinstance(e, APIConnectionError):
        return make_error("API_CONNECTION_FAILED", "Could not connect to AI service.", "system_error", "SYSTEM_ERROR")
    if isinstance(e, BadRequestError):
        return make_error("INVALID_REQUEST", "AI service rejected the request. Please contact support.", "system_error")
    logging.exception("Unexpected extraction error")
    return make_error("UNEXPECTED_SYSTEM_FAILURE", "Unexpected AI extraction failure.", "system_error", "SYSTEM_ERROR")
