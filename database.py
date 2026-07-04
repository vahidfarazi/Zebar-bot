"""
database.py

Handles all database connections and schema initialization.
No business logic allowed.
"""

import sqlite3
from typing import Optional

DB_PATH = "azarakhsh.db"


# -----------------------------
# Connection
# -----------------------------
def get_connection() -> sqlite3.Connection:
    """
    Create and return database connection.
    """

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# -----------------------------
# Initialize Database
# -----------------------------
def init_database() -> None:
    """
    Create all required tables if they don't exist.
    """

    conn = get_connection()
    cursor = conn.cursor()

    # USERS table (includes state for conversation tracking)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER UNIQUE,
            name TEXT,
            username TEXT,
            role TEXT DEFAULT 'USER',
            state TEXT DEFAULT 'MAIN_MENU',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()
