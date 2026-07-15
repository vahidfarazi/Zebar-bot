"""
database/connection.py

PostgreSQL connection manager.
"""

import os

import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row


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
# Close Connection
# -------------------------------------------------

def close_connection(connection=None):
    """
    Close PostgreSQL connection safely.
    """

    if connection:

        try:
            connection.close()

        except Exception:
            pass


# -------------------------------------------------
# Test Connection
# -------------------------------------------------

def init_database():

    connection = None

    try:

        connection = get_connection()

        with connection.cursor() as cursor:

            cursor.execute(
                "SELECT 1"
            )

        print(
            "DATABASE CONNECTION OK"
        )

        return True

    except Exception as e:

        print(
            "DATABASE CONNECTION FAILED:",
            e,
        )

        raise

    finally:

        close_connection(
            connection
        )
