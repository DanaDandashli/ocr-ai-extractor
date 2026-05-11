from db.connection import get_connection


def export_to_db(data):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO invoices (
                invoice_number,
                invoice_date,
                vendor,
                customer,
                subtotal,
                discount,
                shipping,
                tax,
                total,
                currency
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            data.get("invoice_number"),
            data.get("date"),
            data.get("vendor"),
            data.get("customer"),
            data.get("subtotal"),
            data.get("discount"),
            data.get("shipping"),
            data.get("tax"),
            data.get("total"),
            data.get("currency", "USD")
        ))

        invoice_id = cur.fetchone()[0]

        for item in data.get("items", []):
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
