import os
import json
from app.file_naming import generate_filename

CSS = """
<style>
body{font-family:Arial,sans-serif;padding:40px;background:#f5f5f5}
.container{background:#fff;padding:30px;border-radius:10px;max-width:900px;margin:auto}
h1,h2{color:#333}
table{width:100%;border-collapse:collapse;margin-top:20px}
th,td{border:1px solid #ddd;padding:12px;text-align:left}
th{background:#f0f0f0}
.section{margin-bottom:30px}
pre{background:#f9f9f9;padding:12px;border-radius:6px;font-size:13px;overflow-x:auto}
</style>"""


def _render_value(value) -> str:
    if isinstance(value, (dict, list)):
        return f"<pre>{json.dumps(value, indent=2, ensure_ascii=False)}</pre>"
    return str(value) if value is not None else ""


def _render_table(rows: list) -> str:
    if not rows or not isinstance(rows[0], dict):
        return ""
    headers = list(rows[0].keys())
    head = "".join(f"<th>{h}</th>" for h in headers)
    body = "".join(
        "<tr>" +
        "".join(
            f"<td>{_render_value(row.get(h))}</td>" for h in headers) + "</tr>"
        for row in rows
    )
    return f"<table><tr>{head}</tr>{body}</table>"


def export_to_html(data: dict, output_dir: str) -> None:
    for page in data.get("pages", [data]):
        doc_type = page.get("document_type", "Document")
        sections = ""
        for key, value in page.items():
            if key == "document_type":
                continue
            label = key.replace("_", " ").title()
            if isinstance(value, list) and value and isinstance(value[0], dict):
                sections += f'<div class="section"><h2>{label}</h2>{_render_table(value)}</div>'
            elif isinstance(value, dict):
                rows = "".join(
                    f"<tr><td><b>{k}</b></td><td>{_render_value(v)}</td></tr>" for k, v in value.items())
                sections += f'<div class="section"><h2>{label}</h2><table>{rows}</table></div>'
            else:
                sections += f'<div class="section"><h2>{label}</h2><p>{_render_value(value)}</p></div>'

        html = f"""<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"><title>{doc_type}</title>{CSS}</head>
<body><div class="container"><h1>{doc_type}</h1>{sections}</div></body></html>"""

        path = os.path.join(output_dir, generate_filename(page, "html"))
        open(path, "w", encoding="utf-8").write(html)
        print(f"HTML exported: {path}")
