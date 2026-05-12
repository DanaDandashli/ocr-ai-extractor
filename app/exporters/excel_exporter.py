import os
from openpyxl import Workbook
from utils.file_naming import generate_filename


def export_to_excel(data, output_dir):
    pages = data.get("pages", [data])

    for page in pages:
        filename = generate_filename(page, "xlsx")
        output_path = os.path.join(output_dir, filename)

        wb = Workbook()
        ws = wb.active
        ws.title = "Invoice"

        # Invoice details
        main_fields = ["invoice_number",
                        "date",
                        "vendor_name",
                        "vendor_address",
                        "customer_name",
                        "customer_address",
                        "currency"]
        for field in main_fields:
            ws.append([
                field,
                page.get(field)
            ])

        ws.append([])

        # Items table
        ws.append(["Items"])
        ws.append(["Name", "Quantity", "Unit Price", "Total"])
        for item in page.get("items", []):
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
                page.get(field)
            ])

        wb.save(output_path)

        print(f"Excel exported: {output_path}")
