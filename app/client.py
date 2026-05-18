import os
import json
import mimetypes
import base64
from dotenv import load_dotenv
from openai import OpenAI
from app.handle_errors import handle_llm_exception, safe_parse_json
from app.cleaning import clean_text, cleanup_images
from app.cache import get_cache, set_cache, file_hash, text_hash
from app.file_extractor import pdf_to_images

load_dotenv()

_MODEL = "qwen/qwen3.5-flash-02-23"
_MAX_TOKENS = 4000

document_extraction_prompt = """
You are a precise data extraction engine.
Read the document and extract ALL meaningful data from it.

RULES:
- Detect the document type from its content or header.
- Extract every field exactly as printed. Do not compute, infer, or invent.
- If a value is absent → null.
- If tables exist → extract them as lists of row objects.
- For multi-sheet spreadsheets, wrap sheets under a "sheets" array where each sheet contains a "document_type" field.
- Return ONLY valid JSON. No markdown, no prose, no extra text.

OUTPUT:
Return a single JSON object where keys and values reflect exactly what the document contains.
The structure is fully dynamic — you decide the fields based on the document.

EXAMPLES:
Invoice   → {{"invoice_number": "INV-001", "vendor": "...", "total": 500.0, ...}}
Contract  → {{"parties": [...], "effective_date": "...", "terms": "...", ...}}
Receipt   → {{"store": "...", "date": "...", "items": [...], "total": 12.5, ...}}
Report    → {{"title": "...", "author": "...", "summary": "...", "sections": [...], ...}}
"""

grouping_prompt = """
Given {n} PDF page images, group pages that belong to the same document.
Return ONLY a JSON array of 0-based page index groups.
Example (4 pages: 0-1 together, 2 and 3 separate):
[[0,1],[2],[3]]
"""

_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENAI_API_KEY"),
)


def _encode_image(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def _image_block(path: str) -> dict:
    mime = mimetypes.guess_type(path)[0] or "image/png"
    return {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{_encode_image(path)}"}}


def extract_from_text(text: str) -> dict:
    key = text_hash(text)
    cached = get_cache(key)
    if cached:
        return cached

    try:
        response = _client.chat.completions.create(
            model=_MODEL,
            max_tokens=_MAX_TOKENS,
            temperature=0,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You extract structured data from documents."},
                {"role": "user",
                    "content": f"{document_extraction_prompt}\n\nDocument Text:\n{clean_text(text)}"},
            ],
        )
    except Exception as e:
        return handle_llm_exception(e)

    raw = response.choices[0].message.content

    result = safe_parse_json(raw)
    set_cache(key, result)
    return result


def extract_from_image_group(image_paths: list[str] | str) -> dict:
    if isinstance(image_paths, str):
        image_paths = [image_paths]

    key = file_hash(image_paths[0]) if len(
        image_paths) == 1 else text_hash(str(image_paths))
    cached = get_cache(key)
    if cached:
        return cached

    content = [{"type": "text", "text": document_extraction_prompt}] + \
        [_image_block(p) for p in image_paths]
    try:
        response = _client.chat.completions.create(
            model=_MODEL,
            max_tokens=_MAX_TOKENS,
            temperature=0,
            messages=[{"role": "user", "content": content}],
        )
    except Exception as e:
        return handle_llm_exception(e)

    result = safe_parse_json(response.choices[0].message.content)
    set_cache(key, result)
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


def _group_pages(image_paths: list[str]) -> list[list[int]]:
    n = len(image_paths)
    content = [{"type": "text", "text": grouping_prompt.format(n=n)}]
    for idx, path in enumerate(image_paths):
        content.append(_image_block(path))
        content.append({"type": "text", "text": f"Page index {idx}"})
    try:
        response = _client.chat.completions.create(
            model=_MODEL,
            max_tokens=_MAX_TOKENS,
            temperature=0,
            messages=[{"role": "user", "content": content}],
        )
        groups = json.loads(response.choices[0].message.content.strip())
        all_indices = [i for g in groups for i in g]
        if sorted(all_indices) == list(range(n)):
            return groups
    except Exception:
        pass
    return [[i] for i in range(n)]
