import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "fin.db"
_connection = sqlite3.connect(DB_PATH)
_connection.row_factory = sqlite3.Row

def get_connection():
    return _connection

def get_table(table: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table}")
    return cursor.fetchall()