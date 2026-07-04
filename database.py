"""
database.py

Core database layer for Azarakhsh system.
Responsible only for DB connection and persistence.
"""

import sqlite3
from typing import Optional

DB_PATH = "azarakhsh.db"


# -----------------------------
# Connection
# -----------------------------
def get_connection() -> sqlite3.Connection:
    """
    Create and return a new database connection.
    """

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# -----------------------------
# Initialize Database
# -----------------------------
def init_database() -> None:
    """
    Create required tables if they do not exist.
    """

    conn = get_connection()
    cursor = conn.cursor()

    # USERS TABLE (core identity + state)
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

    # REQUESTS TABLE (minimal foundation for tracking system)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tracking_code TEXT UNIQUE,
            chat_id INTEGER,
            service TEXT,
            sub_service TEXT,
            status TEXT DEFAULT 'NEW',
            priority TEXT DEFAULT 'NORMAL',
            expert_id INTEGER,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


# -----------------------------
# USER: Get or Create (UPsert)
# -----------------------------
def get_or_create_user(chat_id: int, username: str = None, name: str = None, role: str = "USER") -> bool:
    """
    Ensure user exists in DB.
    If not exists → create with default state.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM users WHERE chat_id = ?",
        (chat_id,)
    )

    user = cursor.fetchone()

    if user:
        conn.close()
        return True

    cursor.execute(
        """
        INSERT INTO users (chat_id, username, name, role, state)
        VALUES (?, ?, ?, ?, ?)
        """,
        (chat_id, username, name, role, "MAIN_MENU")
    )

    conn.commit()
    conn.close()
    return True


# -----------------------------
# USER: Get User
# -----------------------------
def get_user(chat_id: int) -> Optional[dict]:
    """
    Retrieve user info by chat_id.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE chat_id = ?",
        (chat_id,)
    )

    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return dict(row)


# -----------------------------
# USER: Update State
# -----------------------------
def update_user_state(chat_id: int, state: str) -> None:
    """
    Update conversation state for user.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE users
        SET state = ?
        WHERE chat_id = ?
        """,
        (state, chat_id)
    )

    conn.commit()
    conn.close()
