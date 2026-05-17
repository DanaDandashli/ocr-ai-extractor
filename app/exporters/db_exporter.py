from app.exporters.db.connection import get_connection


def export_to_db(data):
    pages = data.get("pages", [data])

    for page in pages:
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO invoices (
                    invoice_number,
                    invoice_date,
                    vendor_name,
                    vendor_address,
                    customer_name,
                    customer_address,
                    subtotal,
                    discount,
                    shipping,
                    tax,
                    total,
                    currency
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (
                page.get("invoice_number"),
                page.get("date"),
                page.get("vendor_name"),
                page.get("vendor_address"),
                page.get("customer_name"),
                page.get("customer_address"),
                page.get("subtotal"),
                page.get("discount"),
                page.get("shipping"),
                page.get("tax"),
                page.get("total"),
                page.get("currency", "USD")
            ))

            invoice_id = cur.fetchone()[0]

            for item in page.get("items", []):
                cur.execute("""
                    INSERT INTO invoice_items (
                        invoice_id,
                        name,
                        quantity,
                        unit_price,
                        total
                    )
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    invoice_id,
                    item.get("name"),
                    item.get("quantity", 1),
                    item.get("unit_price"),
                    item.get("total")
                ))

            conn.commit()
            print("Invoice saved to database")

        except Exception as e:
            conn.rollback()
            print("Error:", str(e))

        finally:
            cur.close()
            conn.close()
