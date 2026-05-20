import os
import json
import mimetypes
import base64
from dotenv import load_dotenv
from openai import OpenAI
from app.handle_errors import handle_llm_exception, safe_parse_json
from app.cleaning import clean_text, cleanup_images, remove_none_fields, normalize_date, normalize_currency
from app.cache import get_cache, set_cache, file_hash, text_hash
from app.file_extractor import pdf_to_images
from app.lookup import DOCUMENT_TYPES, CLASSIFICATION_PROMPT, GROUPING_PROMPT, get_prompt

load_dotenv()

_MODEL = "google/gemini-2.5-flash-lite"
_MAX_TOKENS = 40000
_TEMPERATURE = 0.0

_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENAI_API_KEY"),
)


# ── Private helpers ──────────────────────────────────────────────────────
def _encode_image(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def _image_block(path: str) -> dict:
    mime = mimetypes.guess_type(path)[0] or "image/png"
    return {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{_encode_image(path)}"}}


def _normalize_result(result: dict) -> dict:
    """Apply post-processing to any extracted result."""
    result = remove_none_fields(result)

    # Normalize dates
    for field in ("date", "due_date"):
        if field in result:
            result[field] = normalize_date(result[field])

    # Normalize currency
    if "currency" in result:
        result["currency"] = normalize_currency(result["currency"])

    if "pages" in result:
        for page in result["pages"]:
            if "currency" in page:
                page["currency"] = normalize_currency(page["currency"])

    return result


def _group_pages(image_paths: list[str]) -> list[list[int]]:
    n = len(image_paths)
    content = [{"type": "text", "text": GROUPING_PROMPT.format(n=n)}]
    for idx, path in enumerate(image_paths):
        content.append(_image_block(path))
        content.append({"type": "text", "text": f"Page index {idx}"})
    try:
        response = _client.chat.completions.create(
            model=_MODEL,
            max_tokens=_MAX_TOKENS,
            temperature=_TEMPERATURE,
            messages=[{"role": "user", "content": content}],
        )
        groups = json.loads(response.choices[0].message.content.strip())
        all_indices = [i for g in groups for i in g]
        if sorted(all_indices) == list(range(n)):
            return groups
    except Exception:
        pass
    return [[i] for i in range(n)]


# ── Document classification ──────────────────────────────────────────────
def classify_document(content: str | list[dict]) -> str:
    """
    content: plain text string OR a list of OpenAI image_url message blocks.
    Returns a doc type string like 'invoice', 'tender', etc.
    """
    if isinstance(content, str):
        # trim for speed
        user_content = f"{CLASSIFICATION_PROMPT}\n\n{content[:3000]}"
    else:
        # image blocks — prepend the instruction as a text block
        user_content = [
            {"type": "text", "text": CLASSIFICATION_PROMPT}] + content

    try:
        response = _client.chat.completions.create(
            model=_MODEL,
            max_tokens=10,
            temperature=_TEMPERATURE,
            messages=[{"role": "user", "content": user_content}],
        )
        detected = response.choices[0].message.content.strip().lower()
        return detected if detected in DOCUMENT_TYPES else "other"
    except Exception:
        return "other"


# ── Extraction ───────────────────────────────────────────────────────────
def extract_from_text(text: str) -> dict:
    key = text_hash(text)
    cached = get_cache(key)
    if cached:
        return cached

    doc_type = classify_document(text)
    prompt = get_prompt(doc_type)

    try:
        response = _client.chat.completions.create(
            model=_MODEL,
            max_tokens=_MAX_TOKENS,
            temperature=_TEMPERATURE,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You extract structured data from documents."},
                {"role": "user",
                    "content": f"{prompt}\n\nDocument Text:\n{clean_text(text)}"},
            ],
        )
    except Exception as e:
        return handle_llm_exception(e)

    raw = response.choices[0].message.content

    result = safe_parse_json(raw)
    result = _normalize_result(result)
    set_cache(key, result)
    # result["_doc_type"] = doc_type              # handy metadata
    return result


def extract_from_image_group(image_paths: list[str] | str) -> dict:
    if isinstance(image_paths, str):
        image_paths = [image_paths]

    key = file_hash(image_paths[0]) if len(
        image_paths) == 1 else text_hash(str(image_paths))
    cached = get_cache(key)
    if cached:
        return cached

    image_blocks = [_image_block(p) for p in image_paths]
    doc_type = classify_document(image_blocks)  # classify from images
    prompt = get_prompt(doc_type)

    content = [{"type": "text", "text": prompt}] + image_blocks
    try:
        response = _client.chat.completions.create(
            model=_MODEL,
            max_tokens=_MAX_TOKENS,
            temperature=_TEMPERATURE,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You extract structured JSON from document images."},
                {"role": "user", "content": content}
            ],
        )
    except Exception as e:
        return handle_llm_exception(e)

    result = safe_parse_json(response.choices[0].message.content)
    result = _normalize_result(result)
    set_cache(key, result)
    # result["_doc_type"] = doc_type
    return result


def extract_from_pdf(pdf_path: str) -> dict:
    key = file_hash(pdf_path)
    cached = get_cache(key)
    if cached:
        return cached

    images = pdf_to_images(pdf_path)
    try:
        groups = [[0]] if len(images) == 1 else _group_pages(images)
        results = []
        for group in groups:
            result = extract_from_image_group([images[i] for i in group])
            if isinstance(result, dict) and result.get("success") is False:
                return result
            results.append(result)
    finally:
        cleanup_images(images)

    result = results[0] if len(results) == 1 else {"pages": results}
    set_cache(key, result)
    return result
