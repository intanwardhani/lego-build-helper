import sqlite3
from pathlib import Path
from src.vars import DB_PATH

# DB_PATH = Path(__file__).resolve().parents[1] / "dataset" / "lego.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def get_schema(conn: sqlite3.Connection) -> str:
    cursor = conn.cursor()
    cursor.execute("""
        SELECT sql
        FROM sqlite_master
        WHERE type='table'
          AND name NOT LIKE 'sqlite_%'
    """)
    rows = cursor.fetchall()

    return "\n\n".join(row[0] for row in rows if row[0] is not None)