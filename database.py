"""
database.py

Core database layer for Azarakhsh Project.

Responsibilities:
- SQLite connection management
- Table creation
- CRUD operations
- Transactions
- Basic settings storage

NO business logic allowed here.
"""

from __future__ import annotations

import sqlite3
import os
from contextlib import contextmanager
from typing import Any, Generator

from config import Config
from logger import log_system, log_error


class DatabaseManager:
    """
    Central database manager.
    """

    _connection: sqlite3.Connection | None = None

    @classmethod
    def init(cls) -> None:
        """
        Initialize database connection and tables.
        """

        db_path = Config.get("DATABASE_PATH")

        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        cls._connection = sqlite3.connect(
            db_path,
            check_same_thread=False,
        )

        cls._connection.row_factory = sqlite3.Row

        log_system("database", "Database initialized")

        cls._create_tables()

    @classmethod
    def get_connection(cls) -> sqlite3.Connection:
        """
        Return database connection.
        """
        if cls._connection is None:
            cls.init()
        return cls._connection  # type: ignore

    @classmethod
    @contextmanager
    def cursor(cls) -> Generator[sqlite3.Cursor, None, None]:
        """
        Context manager for DB cursor.
        """
        conn = cls.get_connection()
        cursor = conn.cursor()

        try:
            yield cursor
            conn.commit()
        except Exception as e:
            conn.rollback()
            log_error("database", str(e))
            raise

    # ---------------- TABLES ---------------- #

    @classmethod
    def _create_tables(cls) -> None:
        """
        Create required tables.
        """

        with cls.cursor() as cur:

            # USERS
            cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER UNIQUE,
                username TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """)

            # REQUESTS
            cur.execute("""
            CREATE TABLE IF NOT EXISTS requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tracking_code TEXT UNIQUE,
                chat_id INTEGER,
                service TEXT,
                sub_service TEXT,
                status TEXT,
                priority TEXT,
                expert_id INTEGER,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                closed_at TEXT
            )
            """)

            # MESSAGES
            cur.execute("""
            CREATE TABLE IF NOT EXISTS request_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tracking_code TEXT,
                sender_type TEXT,
                message TEXT,
                file_path TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """)

            # EXPERTS
            cur.execute("""
            CREATE TABLE IF NOT EXISTS experts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER UNIQUE,
                name TEXT,
                username TEXT,
                department TEXT,
                active INTEGER DEFAULT 1
            )
            """)

            # SETTINGS
            cur.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
            """)

            # LOGS
            cur.execute("""
            CREATE TABLE IF NOT EXISTS system_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                level TEXT,
                module TEXT,
                message TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """)

        log_system("database", "Tables created successfully")

    # ---------------- GENERIC QUERIES ---------------- #

    @classmethod
    def fetch_one(cls, query: str, params: tuple = ()) -> dict | None:
        with cls.cursor() as cur:
            cur.execute(query, params)
            row = cur.fetchone()
            return dict(row) if row else None

    @classmethod
    def fetch_all(cls, query: str, params: tuple = ()) -> list[dict]:
        with cls.cursor() as cur:
            cur.execute(query, params)
            rows = cur.fetchall()
            return [dict(r) for r in rows]

    @classmethod
    def execute(cls, query: str, params: tuple = ()) -> None:
        with cls.cursor() as cur:
            cur.execute(query, params)


# Convenience functions
def get_one(query: str, params: tuple = ()) -> dict | None:
    return DatabaseManager.fetch_one(query, params)


def get_all(query: str, params: tuple = ()) -> list[dict]:
    return DatabaseManager.fetch_all(query, params)


def run(query: str, params: tuple = ()) -> None:
    DatabaseManager.execute(query, params)
