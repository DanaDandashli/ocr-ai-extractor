import os
import json
import gspread
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials

load_dotenv()

_SCOPE = ["https://spreadsheets.google.com/feeds",
          "https://www.googleapis.com/auth/drive"]


def _flatten_value(value) -> str:
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    return str(value) if value is not None else ""


def _get_client():
    creds = Credentials.from_service_account_info({
        "type":         "service_account",
        "client_email": os.getenv("GOOGLE_CLIENT_EMAIL"),
        "private_key":  os.getenv("GOOGLE_PRIVATE_KEY").replace("\\n", "\n"),
        "token_uri":    "https://oauth2.googleapis.com/token",
    }, scopes=_SCOPE)
    return gspread.authorize(creds)


def export_to_google_sheets(data: dict, sheet_name: str = "Documents") -> None:
    spreadsheet = _get_client().open_by_key(os.getenv("GOOGLE_SHEET_KEY"))

    for i, page in enumerate(data.get("pages", [data])):
        doc_type = str(page.get("document_type", "Document"))
        invoice_number = page.get("invoice_number", "")

        # Build a unique tab title
        if invoice_number:
            tab_title = f"{doc_type} {invoice_number}"
        else:
            tab_title = f"{doc_type} {i + 1}"

        tab_title = tab_title[:100]  # Google Sheets tab title limit

        try:
            ws = spreadsheet.worksheet(tab_title)
            ws.clear()
        except gspread.exceptions.WorksheetNotFound:
            ws = spreadsheet.add_worksheet(title=tab_title, rows=200, cols=20)

        rows = []
        for key, value in page.items():
            if isinstance(value, list) and value and isinstance(value[0], dict):
                rows.append([key.replace("_", " ").title()])
                rows.append(list(value[0].keys()))
                for r in value:
                    rows.append([_flatten_value(v) for v in r.values()])
                rows.append([])
            elif isinstance(value, dict):
                rows.append([key.replace("_", " ").title()])
                for k, v in value.items():
                    rows.append([k, _flatten_value(v)])
                rows.append([])
            else:
                rows.append([key, _flatten_value(value)])

        ws.update("A1", rows)
        print(f"Google Sheets exported: tab '{tab_title}'")
