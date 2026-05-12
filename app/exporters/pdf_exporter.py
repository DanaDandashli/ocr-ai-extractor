import os, fitz
from utils.file_naming import generate_filename


def export_to_pdf(data, output_dir):
    pages = data.get("pages", [data])

    for page_data in pages:
        filename = generate_filename(page_data, "pdf")
        output_path = os.path.join(output_dir, filename)
        doc = fitz.open()
        page = doc.new_page()

        x_start = 50
        y_start = 50
        row_height = 25

        def draw_text(x, y, text, size=10):
            page.insert_text((x, y), str(text), fontsize=size)

        def draw_row(y, cols, col_widths):
            x = x_start
            for i, col in enumerate(cols):
                draw_text(x, y, col)
                x += col_widths[i]

        #Title
        draw_text(250, y_start, "INVOICE", size=18)
        y_start += 40

        #Invoice Information
        # info_headers = ["Field", "Value"]
        info_data = [
            ["Invoice Number", page_data.get("invoice_number")],
            ["Date", page_data.get("date")],
            ["Vendor Name", page_data.get("vendor_name")],
            ["Vendor Address", page_data.get("vendor_address")],
            ["Customer Name", page_data.get("customer_name")],
            ["Customer Address", page_data.get("customer_address")],
            ["Currency", page_data.get("currency")]
        ]

        col_widths = [150, 300]
        # draw_row(y_start, info_headers, col_widths)
        y_start += row_height

        for row in info_data:
            draw_row(y_start, row, col_widths)
            y_start += row_height

        y_start += 20

        #Items Table
        draw_text(x_start, y_start, "Items", size=14)
        y_start += 20

        headers = ["Name", "Qty", "Unit Price", "Total"]
        col_widths = [280, 60, 100, 80]

        draw_row(y_start, headers, col_widths)
        y_start += row_height

        for item in page_data.get("items", []):
            draw_row(
                y_start,
                [
                    item.get("name"),
                    item.get("quantity"),
                    item.get("unit_price"),
                    item.get("total")
                ],
                col_widths
            )
            y_start += row_height

        y_start += 20

        #Summary
        draw_text(x_start, y_start, "Summary", size=14)
        y_start += 20

        summary = [
            ["Subtotal", page_data.get("subtotal")],
            ["Discount", page_data.get("discount")],
            ["Shipping", page_data.get("shipping")],
            ["Tax", page_data.get("tax")],
            ["Total", page_data.get("total")]
        ]

        col_widths = [150, 150]

        for row in summary:
            draw_row(y_start, row, col_widths)
            y_start += row_height

        doc.save(output_path)
        doc.close()

        print(f"PDF exported: {output_path}")
