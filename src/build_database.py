import sqlite3
from vars import DB_PATH, SCHEMA_PATH

def build_database():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA foreign_keys = ON;")

        schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")
        conn.executescript(schema_sql)

        print(f"Database created at {DB_PATH}")

if __name__ == "__main__":
    build_database()
