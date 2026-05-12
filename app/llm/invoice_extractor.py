import os, json, base64
from dotenv import load_dotenv
from openai import OpenAI
from llm.cleaner import clean_text
from llm.schema import invoice_schema
from llm.prompts import invoice_extraction_prompt
from utils.base import parse_json_response
from extractors.pdf_to_image import pdf_to_images


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
    prompt = invoice_extraction_prompt.format(
        schema=json.dumps(invoice_schema, indent=2)
    )
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
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ]
            }
        ]
    )
    #print(response.usage)
    result = response.choices[0].message.content
    #print("\n=== RAW MODEL RESPONSE ===\n")
    #print(result)
    return parse_json_response(result)


def extract_invoice_from_pdf(pdf_path: str) -> dict:
    """
    Full pipeline: PDF -> images -> vision extraction
    """
    images = pdf_to_images(pdf_path)
    results = []
    
    for img in images:
        result = extract_invoice_from_image(img)
        results.append(result)

    # If multi-page invoice -> merge logic
    if len(results) == 1:
        return results[0]

    return {
        "pages": results
    }
