"""
database/connection.py

PostgreSQL connection manager.
"""

import os

import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row


# -------------------------------------------------
# Load Environment
# -------------------------------------------------

load_dotenv()


# -------------------------------------------------
# Get Connection
# -------------------------------------------------

def get_connection():
    """
    Return PostgreSQL connection.
    """

    return psycopg.connect(
        host=os.getenv("PGHOST"),
        port=os.getenv("PGPORT"),
        dbname=os.getenv("PGDATABASE"),
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD"),
        sslmode="require",
        row_factory=dict_row,
    )


# -------------------------------------------------
# Initialize Database
# -------------------------------------------------

def init_database():
    """
    Initialize database connection.

    This function only checks that PostgreSQL
    connection is available and closes it.

    Tables should be created separately.
    """

    conn = None

    try:
        conn = get_connection()

        # تست ساده اتصال
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT 1"
            )

        print(
            "DATABASE CONNECTION OK"
        )

    except Exception as e:

        print(
            "DATABASE CONNECTION FAILED:",
            e,
        )

        raise

    finally:

        if conn:

            conn.close()
