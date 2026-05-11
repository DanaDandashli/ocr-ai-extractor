import os, json
from dotenv import load_dotenv
from openai import OpenAI
from llm.cleaner import clean_text, normalize_currency
from llm.schema import invoice_schema
from llm.prompts import invoice_extraction_prompt

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENAI_API_KEY"),
)


"""
    Convert extracted invoice text into structured JSON using LLM.
"""
def extract_invoice_json(text: str) -> dict:
    prompt = invoice_extraction_prompt.format(
        schema=json.dumps(invoice_schema, indent=2),
        text=clean_text(text)
    )
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b:free",
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": "You extract structured invoice data."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    #print(response.usage)

    result = response.choices[0].message.content

    try:
        data =  json.loads(result)
        data["currency"] = normalize_currency(data.get("currency"))
        return data

    except json.JSONDecodeError:
        raise ValueError(
            f"Invalid JSON returned by LLM:\n{result}"
        )
