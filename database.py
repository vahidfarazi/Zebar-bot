"""
database.py

Responsible for all database operations:
- connection
- schema creation
- CRUD operations
- transactions
"""

import sqlite3
from typing import Any, Optional
from logger import log_system, log_error
from config import Config


# -----------------------------
# Database Connection
# -----------------------------
_DB_PATH = Config.get("DB_PATH", "azarakhsh.db")


def get_connection() -> sqlite3.Connection:
    """
    Create and return a database connection.
    """
    conn = sqlite3.connect(_DB_PATH, check_same_thread=False)
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

        # ---------------- USERS ----------------
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER UNIQUE,
            username TEXT,
            full_name TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # ---------------- REQUESTS ----------------
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tracking_code TEXT UNIQUE,
            user_chat_id INTEGER,
            service TEXT,
            sub_service TEXT,
            status TEXT,
            priority TEXT DEFAULT 'NORMAL',
            expert_id INTEGER,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            closed_at TEXT
        )
        """)

        cursor.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_requests_tracking
        ON requests(tracking_code)
        """)

        # ---------------- REQUEST MESSAGES ----------------
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS request_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tracking_code TEXT,
            sender_type TEXT,
            message TEXT,
            file_path TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # ---------------- EXPERTS ----------------
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS experts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER UNIQUE,
            name TEXT,
            username TEXT,
            department TEXT,
            active INTEGER DEFAULT 1
        )
        """)

        # ---------------- ADMINS ----------------
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER UNIQUE,
            role TEXT DEFAULT 'ADMIN'
        )
        """)

        # ---------------- SETTINGS ----------------
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
        """)

        # ---------------- LOGS ----------------
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS system_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            level TEXT,
            module TEXT,
            action TEXT,
            description TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """)

        conn.commit()
        conn.close()

        log_system("database", "init", "Database initialized successfully")

    except Exception as e:
        log_error("database", "init_failed", str(e))
        raise


# -----------------------------
# Generic Query Executor
# -----------------------------
def execute(query: str, params: tuple = ()) -> None:
    """
    Execute INSERT/UPDATE/DELETE queries.
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(query, params)
        conn.commit()
    except Exception as e:
        log_error("database", "execute_error", str(e))
        raise
    finally:
        conn.close()


def fetch_one(query: str, params: tuple = ()) -> Optional[sqlite3.Row]:
    """
    Fetch single record.
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(query, params)
        return cursor.fetchone()
    except Exception as e:
        log_error("database", "fetch_one_error", str(e))
        return None
    finally:
        conn.close()


def fetch_all(query: str, params: tuple = ()) -> list:
    """
    Fetch all records.
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(query, params)
        return cursor.fetchall()
    except Exception as e:
        log_error("database", "fetch_all_error", str(e))
        return []
    finally:
        conn.close()
