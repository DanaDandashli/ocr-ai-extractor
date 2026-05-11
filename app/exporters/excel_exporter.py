import os
from openpyxl import Workbook
from utils.file_naming import generate_filename


def export_to_excel(data, output_dir):

    filename = generate_filename(data, "xlsx")
    output_path = os.path.join(output_dir, filename)

    wb = Workbook()
    ws = wb.active
    ws.title = "Invoice"

    # Invoice details
    ws.append(["Field", "Value"])
    main_fields = ["invoice_number", "date", "vendor", "customer", "currency"]
    for field in main_fields:
        ws.append([
            field,
            data.get(field)
        ])

    ws.append([])

    # Items table
    ws.append(["Items"])
    ws.append(["Name", "Quantity", "Unit Price", "Total"])
    for item in data.get("items", []):
        ws.append([
            item.get("name"),
            item.get("quantity"),
            item.get("unit_price"),
            item.get("total")
        ])

    ws.append([])

    summary_fields = ["subtotal", "discount", "shipping", "tax", "total"]
    for field in summary_fields:
        ws.append([
            field,
            data.get(field)
        ])

    wb.save(output_path)

    print(f"Excel exported: {output_path}")
