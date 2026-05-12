import os
from docx import Document
from docx.shared import Inches
from utils.file_naming import generate_filename


def export_to_docx(data, output_dir):
    pages = data.get("pages", [data])

    for page in pages:
        filename = generate_filename(page, "docx")
        output_path = os.path.join(output_dir, filename)
        doc = Document()
        doc.add_heading("INVOICE", level=1)

        doc.add_heading("Invoice Details", level=2)
        doc.add_paragraph(f"Invoice Number: {page.get('invoice_number')}")
        doc.add_paragraph(f"Date: {page.get('date')}")
        doc.add_paragraph(f"Vendor Name: {page.get('vendor_name')}")
        doc.add_paragraph(f"Vendor Address: {page.get('vendor_address')}")
        doc.add_paragraph(f"Customer Name: {page.get('customer_name')}")
        doc.add_paragraph(f"Customer Address: {page.get('customer_address')}")
        doc.add_paragraph(f"Currency: {page.get('currency')}")

        doc.add_heading("Items", level=2)
        table = doc.add_table(rows=1, cols=4)
        table.style = "Table Grid"
        header_cells = table.rows[0].cells
        header_cells[0].text = "Name"
        header_cells[1].text = "Quantity"
        header_cells[2].text = "Unit Price"
        header_cells[3].text = "Total"
        
        header_cells[0].width = Inches(3.0)
        header_cells[1].width = Inches(0.8)
        header_cells[2].width = Inches(1.2)
        header_cells[3].width = Inches(1.0)

        for item in page.get("items", []):
            row_cells = table.add_row().cells
            row_cells[0].text = str(item.get("name"))
            row_cells[1].text = str(item.get("quantity"))
            row_cells[2].text = str(item.get("unit_price"))
            row_cells[3].text = str(item.get("total"))

            row_cells[0].width = Inches(3.0)
            row_cells[1].width = Inches(0.8)
            row_cells[2].width = Inches(1.2)
            row_cells[3].width = Inches(1.0)

        doc.add_heading("Summary", level=2)
        doc.add_paragraph(f"Subtotal: {page.get('subtotal')}")
        doc.add_paragraph(f"Discount: {page.get('discount')}")
        doc.add_paragraph(f"Shipping: {page.get('shipping')}")
        doc.add_paragraph(f"Tax: {page.get('tax')}")
        doc.add_paragraph(f"Total: {page.get('total')}")

        doc.save(output_path)

        print(f"DOCX exported: {output_path}")
