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
    Return SQLite connection.
    """

    os.makedirs(DB_DIRECTORY, exist_ok=True)

    print("DB PATH:", DB_PATH)
    
    connection = sqlite3.connect(
        DB_PATH,
        check_same_thread=False,
    )

    connection.row_factory = sqlite3.Row

    connection.execute("PRAGMA foreign_keys = ON")

    return connection
