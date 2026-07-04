"""
database.py

Core database layer for Azarakhsh system.
Responsible for:
- connection
- schema creation
- basic CRUD operations
"""

import sqlite3
from typing import Any, Optional
from logger import log_system, log_error


# -----------------------------
# Database Path
# -----------------------------
DB_PATH = "database/azarakhsh.db"


# -----------------------------
# Connection
# -----------------------------
def get_connection() -> sqlite3.Connection:
    """
    Create and return DB connection.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


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

        # -------------------------
        # USERS TABLE
        # -------------------------
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            chat_id INTEGER PRIMARY KEY,
            username TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # -------------------------
        # REQUESTS TABLE
        # -------------------------
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tracking_code TEXT UNIQUE,
            chat_id INTEGER,
            title TEXT,
            description TEXT,
            status TEXT DEFAULT 'OPEN',
            priority TEXT DEFAULT 'NORMAL',
            expert_id INTEGER,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # -------------------------
        # EXPERTS TABLE
        # -------------------------
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS experts (
            chat_id INTEGER PRIMARY KEY,
            name TEXT,
            username TEXT,
            department TEXT,
            is_active INTEGER DEFAULT 1
        )
        """)

        # -------------------------
        # ADMINS TABLE
        # -------------------------
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            chat_id INTEGER PRIMARY KEY
        )
        """)

        # -------------------------
        # HOLIDAYS TABLE
        # -------------------------
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS holidays (
            holiday_date TEXT PRIMARY KEY,
            enabled INTEGER DEFAULT 1
        )
        """)

        # -------------------------
        # SETTINGS TABLE
        # -------------------------
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
        """)

        # -------------------------
        # LOGS TABLE
        # -------------------------
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
            level TEXT,
            module TEXT,
            action TEXT,
            user_id TEXT,
            description TEXT
        )
        """)

        conn.commit()
        conn.close()

        log_system("database", "init", "Database initialized successfully")

    except Exception as e:
        log_error("database", "init_failed", str(e))
        raise


# -----------------------------
# Get Request by Tracking
# -----------------------------
def get_request_by_tracking(tracking_code: str) -> Optional[dict]:
    """
    Fetch request using tracking code.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM requests WHERE tracking_code = ?",
        (tracking_code,)
    )

    row = cursor.fetchone()
    conn.close()

    return dict(row) if row else None


# -----------------------------
# Insert Request
# -----------------------------
def insert_request(tracking_code: str, chat_id: int, title: str, description: str) -> bool:
    """
    Create new request.
    """

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO requests (tracking_code, chat_id, title, description)
        VALUES (?, ?, ?, ?)
        """, (tracking_code, chat_id, title, description))

        conn.commit()
        conn.close()

        return True

    except Exception as e:
        log_error("database", "insert_request", str(e))
        return False


# -----------------------------
# Update Request Status
# -----------------------------
def update_request_status(request_id: int, status: str) -> bool:
    """
    Update request status.
    """

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE requests
        SET status = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """, (status, request_id))

        conn.commit()
        conn.close()

        return True

    except Exception as e:
        log_error("database", "update_status", str(e))
        return False


# -----------------------------
# Get Setting
# -----------------------------
def get_setting(key: str) -> Optional[str]:
    """
    Get system setting value.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT value FROM settings WHERE key = ?",
        (key,)
    )

    row = cursor.fetchone()
    conn.close()

    return row["value"] if row else None
