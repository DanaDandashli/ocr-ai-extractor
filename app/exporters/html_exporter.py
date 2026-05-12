import os
from utils.file_naming import generate_filename


def export_to_html(data, output_dir):
    pages = data.get("pages", [data])

    for page in pages:
        filename = generate_filename(page, "html")
        output_path = os.path.join(output_dir, filename)

        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Invoice</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    padding: 40px;
                    background: #f5f5f5;
                }}

                .container {{
                    background: white;
                    padding: 30px;
                    border-radius: 10px;
                    max-width: 900px;
                    margin: auto;
                }}

                h1, h2 {{
                    color: #333;
                }}

                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                }}

                th, td {{
                    border: 1px solid #ddd;
                    padding: 12px;
                    text-align: left;
                }}

                th {{
                    background-color: #f0f0f0;
                }}

                .section {{
                    margin-bottom: 30px;
                }}
            </style>
        </head>

        <body>
            <div class="container">
                <h1>Invoice</h1>
                <div class="section">
                    <h2>Invoice Information</h2>
                    <table>
                        <tr>
                            <th>Info</th>
                            <th>Value</th>
                        </tr>
                        <tr>
                            <td>Invoice Number</td>
                            <td>{page.get("invoice_number")}</td>
                        </tr>
                        <tr>
                            <td>Date</td>
                            <td>{page.get("date")}</td>
                        </tr>
                        <tr>
                            <td>Vendor Name</td>
                            <td>{page.get("vendor_name")}</td>
                        </tr>
                        <tr>
                            <td>Vendor Address</td>
                            <td>{page.get("vendor_address")}</td>
                        </tr>
                        <tr>
                            <td>Customer Name</td>
                            <td>{page.get("customer_name")}</td>
                        </tr>
                        <tr>
                            <td>Customer Address</td>
                            <td>{page.get("customer_address")}</td>
                        </tr>
                        <tr>
                            <td>Currency</td>
                            <td>{page.get("currency")}</td>
                        </tr>
                    </table>
                </div>
                <div class="section">
                    <h2>Items</h2>
                    <table>
                        <tr>
                            <th>Name</th>
                            <th>Quantity</th>
                            <th>Unit Price</th>
                            <th>Total</th>
                        </tr>
        """
        for item in page.get("items", []):
            html += f"""
                        <tr>
                            <td>{item.get("name")}</td>
                            <td>{item.get("quantity")}</td>
                            <td>{item.get("unit_price")}</td>
                            <td>{item.get("total")}</td>
                        </tr>
            """
        html += f"""
                    </table>
                </div>
                <div class="section">
                    <h2>Financial Summary</h2>
                    <table>
                        <tr>
                            <th>Field</th>
                            <th>Value</th>
                        </tr>
                        <tr>
                            <td>Subtotal</td>
                            <td>{page.get("subtotal")}</td>
                        </tr>
                        <tr>
                            <td>Discount</td>
                            <td>{page.get("discount")}</td>
                        </tr>
                        <tr>
                            <td>Shipping</td>
                            <td>{page.get("shipping")}</td>
                        </tr>
                        <tr>
                            <td>Tax</td>
                            <td>{page.get("tax")}</td>
                        </tr>
                        <tr>
                            <td>Total</td>
                            <td>{page.get("total")}</td>
                        </tr>
                    </table>
                </div>
            </div>
        </body>
        </html>
        """
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"HTML exported: {output_path}")
