"""
database/connection.py

Database connection manager for Azarakhsh.
"""

import os
import sqlite3

DB_DIRECTORY = "database"
DB_NAME = "azarakhsh.db"
DB_PATH = os.path.join(DB_DIRECTORY, DB_NAME)


def get_connection() -> sqlite3.Connection:
    """
    Create and return SQLite connection.
    """

    os.makedirs(DB_DIRECTORY, exist_ok=True)

    connection = sqlite3.connect(DB_PATH)

    connection.row_factory = sqlite3.Row

    connection.execute("PRAGMA foreign_keys = ON")

    return connection
