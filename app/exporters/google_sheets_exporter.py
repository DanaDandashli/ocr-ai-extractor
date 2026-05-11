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
    sheet = client.open_by_key(os.getenv("GOOGLE_SHEET_KEY")).sheet1

    sheet.clear()
    row = 1

    sheet.update(f"A{row}", [["Field", "Value"]])
    row += 1

    main_fields = [
        "invoice_number",
        "date",
        "vendor",
        "customer",
        "currency"
    ]

    for field in main_fields:
        sheet.update(
            f"A{row}:B{row}",
            [[field, data.get(field)]]
        )
        row += 1

    row += 2  

    sheet.update(
        f"A{row}:D{row}",
        [["Name", "Quantity", "Unit Price", "Total"]]
    )
    row += 1

    for item in data.get("items", []):
        sheet.update(
            f"A{row}:D{row}",
            [[
                item.get("name"),
                item.get("quantity"),
                item.get("unit_price"),
                item.get("total")
            ]]
        )
        row += 1

    row += 2

    summary_fields = [
        "subtotal",
        "discount",
        "shipping",
        "tax",
        "total"
    ]
    for field in summary_fields:
        sheet.update(
            f"A{row}:B{row}",
            [[field, data.get(field)]]
        )
        row += 1

    print("Google Sheets exported (Excel-style layout).")
