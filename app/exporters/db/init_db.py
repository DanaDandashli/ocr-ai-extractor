import os
from app.exporters.db.connection import get_connection


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    base_dir = os.path.dirname(__file__)
    schema_path = os.path.join(base_dir, "schema.sql")

    with open(schema_path, "r") as f:
        cur.execute(f.read())

    conn.commit()
    cur.close()
    conn.close()

    print("Database initialized successfully")


if __name__ == "__main__":
    init_db()
