import os
import json
from openpyxl import Workbook
from app.file_naming import generate_filename


def _flatten_value(value) -> str:
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    return value if value is not None else ""


def export_to_excel(data: dict, output_dir: str) -> None:
    for page in data.get("pages", [data]):
        wb = Workbook()
        ws = wb.active
        ws.title = page.get("document_type", "Document")[:31]

        for key, value in page.items():
            if isinstance(value, list) and value and isinstance(value[0], dict):
                ws.append([])
                ws.append([key.replace("_", " ").title()])
                ws.append(list(value[0].keys()))
                for row in value:
                    ws.append([_flatten_value(v) for v in row.values()])
            elif isinstance(value, dict):
                ws.append([])
                ws.append([key.replace("_", " ").title()])
                for k, v in value.items():
                    ws.append([k, _flatten_value(v)])
            else:
                ws.append([key, _flatten_value(value)])

        path = os.path.join(output_dir, generate_filename(page, "xlsx"))
        wb.save(path)
        print(f"Excel exported: {path}")
