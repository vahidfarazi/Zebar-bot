"""
database/connection.py

PostgreSQL connection manager.
"""

from config import Config
import psycopg
from psycopg.rows import dict_row


def get_connection():
    """
    Return PostgreSQL connection.
    """

    return psycopg.connect(
        host=Config.get_str("PGHOST"),
        port=Config.get_str("PGPORT"),
        dbname=Config.get_str("PGDATABASE"),
        user=Config.get_str("PGUSER"),
        password=Config.get_str("PGPASSWORD"),
        sslmode="require",
        row_factory=dict_row,
    )
