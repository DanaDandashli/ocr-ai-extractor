import os
from docx import Document
from utils.file_naming import generate_filename


def export_to_docx(data, output_dir):

    filename = generate_filename(data, "docx")
    output_path = os.path.join(output_dir, filename)
    doc = Document()
    doc.add_heading("INVOICE", level=1)

    doc.add_heading("Invoice Details", level=2)
    doc.add_paragraph(f"Invoice Number: {data.get('invoice_number')}")
    doc.add_paragraph(f"Date: {data.get('date')}")
    doc.add_paragraph(f"Vendor: {data.get('vendor')}")
    doc.add_paragraph(f"Customer: {data.get('customer')}")
    doc.add_paragraph(f"Currency: {data.get('currency')}")

    doc.add_heading("Items", level=2)
    table = doc.add_table(rows=1, cols=4)
    header_cells = table.rows[0].cells
    header_cells[0].text = "Name"
    header_cells[1].text = "Quantity"
    header_cells[2].text = "Unit Price"
    header_cells[3].text = "Total"

    for item in data.get("items", []):

        row_cells = table.add_row().cells
        row_cells[0].text = str(item.get("name"))
        row_cells[1].text = str(item.get("quantity"))
        row_cells[2].text = str(item.get("unit_price"))
        row_cells[3].text = str(item.get("total"))

    doc.add_heading("Summary", level=2)
    doc.add_paragraph(f"Subtotal: {data.get('subtotal')}")
    doc.add_paragraph(f"Discount: {data.get('discount')}")
    doc.add_paragraph(f"Shipping: {data.get('shipping')}")
    doc.add_paragraph(f"Tax: {data.get('tax')}")
    doc.add_paragraph(f"Total: {data.get('total')}")

    doc.save(output_path)

    print(f"DOCX exported: {output_path}")
