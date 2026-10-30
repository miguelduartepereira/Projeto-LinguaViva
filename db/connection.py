# db/connection.py
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "linguaviva.db"
SCHEMA_PATH = Path(__file__).parent / "schema.sql"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def inicializar_bd():
    schema = SCHEMA_PATH.read_text(encoding="utf-8")
    with get_connection() as conn:
        conn.executescript(schema)
