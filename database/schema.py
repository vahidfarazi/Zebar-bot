"""
database/schema.py

Database schema initialization.
"""

from .connection import get_connection


def init_database() -> None:
    """
    Create all required database tables.
    """

    connection = get_connection()

    try:

        cursor = connection.cursor()

        # -----------------------------
        # Users
        # -----------------------------
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            chat_id INTEGER PRIMARY KEY,
            username TEXT,
            full_name TEXT,
            role TEXT DEFAULT 'USER',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # -----------------------------
        # Requests
        # -----------------------------
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS requests (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            tracking_code TEXT UNIQUE NOT NULL,

            chat_id INTEGER NOT NULL,

            service TEXT NOT NULL,

            sub_service TEXT,

            status TEXT DEFAULT 'NEW',

            priority TEXT DEFAULT 'NORMAL',

            expert_id INTEGER,

            expert_chat_id INTEGER,

            expert_message_id INTEGER,

            created_at TEXT DEFAULT CURRENT_TIMESTAMP,

            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,

            closed_at TEXT

        )
        """)

        # -----------------------------
        # Request Messages
        # -----------------------------
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS request_messages (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            tracking_code TEXT NOT NULL,

            sender_type TEXT NOT NULL,

            sender_id INTEGER NOT NULL,

            message_type TEXT NOT NULL,

            message TEXT NOT NULL,

            created_at TEXT DEFAULT CURRENT_TIMESTAMP

        )
        """)

        # -----------------------------
        # Experts
        # -----------------------------
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS experts (

            chat_id INTEGER PRIMARY KEY,

            name TEXT,

            username TEXT,

            department TEXT,

            is_active INTEGER DEFAULT 1

        )
        """)

        # -----------------------------
        # Admins
        # -----------------------------
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS admins (

            chat_id INTEGER PRIMARY KEY

        )
        """)

        # -----------------------------
        # Settings
        # -----------------------------
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (

            key TEXT PRIMARY KEY,

            value TEXT

        )
        """)

        # -----------------------------
        # Holidays
        # -----------------------------
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS holidays (

            holiday_date TEXT PRIMARY KEY,

            enabled INTEGER DEFAULT 1

        )
        """)

        # -----------------------------
        # System Logs
        # -----------------------------
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS system_logs (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            created_at TEXT DEFAULT CURRENT_TIMESTAMP,

            level TEXT NOT NULL,

            module TEXT NOT NULL,

            action TEXT NOT NULL,

            description TEXT

        )
        """)

        connection.commit()

    finally:

        connection.close()
