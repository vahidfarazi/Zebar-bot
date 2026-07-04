"""
database.py

Core database layer for Azarakhsh system.

Responsible for:
- database connection
- schema initialization
- generic SQL helpers
- request operations
"""

import os
import sqlite3
from typing import Any, Optional

from logger import log_system, log_error


# -----------------------------
# Database Path
# -----------------------------
DB_DIRECTORY = "database"
DB_PATH = os.path.join(DB_DIRECTORY, "azarakhsh.db")


# -----------------------------
# Connection
# -----------------------------
def get_connection() -> sqlite3.Connection:
    """
    Create database connection.
    """

    os.makedirs(DB_DIRECTORY, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    return conn


# -----------------------------
# Generic Execute
# -----------------------------
def execute(query: str, params: tuple = ()) -> None:
    """
    Execute INSERT / UPDATE / DELETE.
    """

    conn = get_connection()

    try:

        conn.execute(query, params)
        conn.commit()

    finally:

        conn.close()


# -----------------------------
# Generic Fetch One
# -----------------------------
def fetch_one(
    query: str,
    params: tuple = (),
) -> Optional[sqlite3.Row]:
    """
    Fetch one row.
    """

    conn = get_connection()

    try:

        cursor = conn.execute(query, params)

        return cursor.fetchone()

    finally:

        conn.close()


# -----------------------------
# Generic Fetch All
# -----------------------------
def fetch_all(
    query: str,
    params: tuple = (),
) -> list[sqlite3.Row]:
    """
    Fetch all rows.
    """

    conn = get_connection()

    try:

        cursor = conn.execute(query, params)

        return cursor.fetchall()

    finally:

        conn.close()


# -----------------------------
# Initialize Database
# -----------------------------
def init_database() -> None:
    """
    Create all required tables.
    """

    try:

        conn = get_connection()
        cursor = conn.cursor()

        # Users
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            chat_id INTEGER PRIMARY KEY,
            username TEXT,
            full_name TEXT,
            role TEXT DEFAULT 'USER',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Requests
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tracking_code TEXT UNIQUE NOT NULL,
            chat_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT DEFAULT 'OPEN',
            priority TEXT DEFAULT 'NORMAL',
            expert_id INTEGER,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Experts
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS experts (
            chat_id INTEGER PRIMARY KEY,
            name TEXT,
            username TEXT,
            department TEXT,
            is_active INTEGER DEFAULT 1
        )
        """)

        # Admins
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            chat_id INTEGER PRIMARY KEY
        )
        """)

        # Holidays
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS holidays (
            holiday_date TEXT PRIMARY KEY,
            enabled INTEGER DEFAULT 1
        )
        """)

        # Settings
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
        """)

        # Logs
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS system_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            level TEXT,
            module TEXT,
            action TEXT,
            description TEXT
        )
        """)

        conn.commit()
        conn.close()

        log_system(
            "database",
            "init",
            "Database initialized successfully",
        )

    except Exception as exc:

        log_error(
            "database",
            "init_database",
            str(exc),
        )

        raise


# -----------------------------
# Request Helpers
# -----------------------------
def get_request_by_tracking(
    tracking_code: str,
) -> Optional[dict]:
    """
    Get request by tracking code.
    """

    row = fetch_one(
        """
        SELECT *
        FROM requests
        WHERE tracking_code = ?
        """,
        (tracking_code,),
    )

    return dict(row) if row else None


def insert_request(
    tracking_code: str,
    chat_id: int,
    title: str,
    description: str,
) -> bool:
    """
    Insert new request.
    """

    try:

        execute(
            """
            INSERT INTO requests
            (
                tracking_code,
                chat_id,
                title,
                description
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                tracking_code,
                chat_id,
                title,
                description,
            ),
        )

        return True

    except Exception as exc:

        log_error(
            "database",
            "insert_request",
            str(exc),
        )

        return False


def update_request_status(
    request_id: int,
    status: str,
) -> bool:
    """
    Update request status.
    """

    try:

        execute(
            """
            UPDATE requests
            SET
                status = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (
                status,
                request_id,
            ),
        )

        return True

    except Exception as exc:

        log_error(
            "database",
            "update_request_status",
            str(exc),
        )

        return False


# -----------------------------
# Settings
# -----------------------------
def get_setting(
    key: str,
) -> Optional[str]:
    """
    Get setting value.
    """

    row = fetch_one(
        """
        SELECT value
        FROM settings
        WHERE key = ?
        """,
        (key,),
    )

    return row["value"] if row else None
