import json
from app.exporters.db.connection import get_connection


def export_to_db(data: dict) -> None:
    for page in data.get("pages", data.get("sheets", [data])):
        doc_type = page.get("document_type", "unknown")
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO documents (document_type, data)
                VALUES (%s, %s)
            """, (
                doc_type,
                json.dumps(page, ensure_ascii=False)
            ))
            conn.commit()
            print(f"Document saved to database: {doc_type}")
        except Exception as e:
            conn.rollback()
            print("Error:", e)
        finally:
            cur.close()
            conn.close()
