import json
from llm.cleaner import normalize_currency


def parse_json_response(result: str) -> dict:
    try:
        data = json.loads(result)
        data["currency"] = normalize_currency(data.get("currency"))
        return data

    except json.JSONDecodeError:
        raise ValueError(
            f"Invalid JSON returned by model:\n{result}"
        )
