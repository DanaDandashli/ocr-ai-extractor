import os, gspread
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials


def export_to_google_sheets(data, sheet_name="Invoices"):

    load_dotenv()
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_info({
        "type": "service_account",
        "client_email": os.getenv("GOOGLE_CLIENT_EMAIL"),
        "private_key": os.getenv("GOOGLE_PRIVATE_KEY").replace("\\n", "\n"),
        "token_uri": "https://oauth2.googleapis.com/token"
    }, scopes=scope)

    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(os.getenv("GOOGLE_SHEET_KEY"))
    pages = data.get("pages", [data])

    for page in pages:
        invoice_number = str(page.get("invoice_number", "unknown"))

        try:
            ws = spreadsheet.worksheet(invoice_number)
            ws.clear()
        except gspread.exceptions.WorksheetNotFound:
            ws = spreadsheet.add_worksheet(
                title=invoice_number, rows=100, cols=20)

        rows = []

        # Invoice details
        main_fields = [
            "invoice_number", "date", "vendor_name", "vendor_address",
            "customer_name", "customer_address", "currency"
        ]
        for field in main_fields:
            rows.append([field, str(page.get(field) or "")])

        rows.append([])

        # Items table
        rows.append(["Name", "Quantity", "Unit Price", "Total"])
        for item in page.get("items", []):
            rows.append([
                str(item.get("name") or ""),
                item.get("quantity"),
                item.get("unit_price"),
                item.get("total")
            ])

        # Summary
        summary_fields = ["subtotal", "discount", "shipping", "tax", "total"]
        for field in summary_fields:
            rows.append([field, str(page.get(field) or "")])

        ws.update(f"A1", rows)

        print(f"Google Sheets exported: tab '{invoice_number}'")
