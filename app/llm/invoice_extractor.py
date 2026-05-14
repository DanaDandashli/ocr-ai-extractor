import os, json, base64, mimetypes
from dotenv import load_dotenv
from openai import OpenAI
from llm.cleaner import clean_text
from llm.schema import invoice_schema
from llm.prompts import invoice_extraction_prompt
from utils.base import parse_json_response
from extractors.pdf_to_image import pdf_to_images
from utils.handle_errors import handle_llm_exception

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENAI_API_KEY"),
)


"""
    Convert extracted invoice text into structured JSON using LLM.
"""
def extract_invoice_json(text: str) -> dict:
    cleaned_text = clean_text(text)
    prompt = invoice_extraction_prompt.format(
        schema=json.dumps(invoice_schema, indent=2),
    )
    try:
        response = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            temperature=0,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": "You extract structured invoice data."
                },
                {
                    "role": "user",
                    "content": f"{prompt}\n\nInvoice Text:\n{cleaned_text}"
                }
            ]
        )
    
    except Exception as e:
        return handle_llm_exception(e)

    #print(response.usage)
    result = response.choices[0].message.content

    return parse_json_response(result)


# Vision extractor:
def encode_image(image_path: str) -> str:
    """Convert image to base64 string"""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def extract_invoice_from_image(image_path: str) -> dict:
    """
    Sends image to vision model and returns structured JSON.
    """
    base64_image = encode_image(image_path)
    mime = mimetypes.guess_type(image_path)[0] or "image/png"
    prompt = invoice_extraction_prompt.format(
        schema=json.dumps(invoice_schema, indent=2)
    )
    try:
        response = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            temperature=0,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime};base64,{base64_image}"
                            }
                        }
                    ]
                }
            ]
        )
    
    except Exception as e:
        return handle_llm_exception(e)
    
    #print(response.usage)
    result = response.choices[0].message.content
    
    return parse_json_response(result)


def cleanup_images(image_paths: list):
    """Remove temporary page images after extraction."""
    for path in image_paths:
        try:
            if os.path.exists(path):
                os.remove(path)
        except OSError as e:
            print(f"[WARN] Could not delete temp file {path}: {e}")


def extract_invoice_from_pdf(pdf_path: str) -> dict:
    """
    Full pipeline: PDF -> images -> vision extraction
    """
    images = pdf_to_images(pdf_path)
    results = []
    try:
        for img in images:
            result = extract_invoice_from_image(img)
            if isinstance(result, dict) and result.get("success") is False:
                return result
            
            results.append(result)
    
    finally:
        cleanup_images(images)

    # If multi-page invoice -> merge logic
    if len(results) == 1:
        return results[0]

    return {
        "pages": results
    }
