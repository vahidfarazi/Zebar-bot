"""
database/connection.py

PostgreSQL connection manager.
"""

import os

import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row

# بارگذاری .env
load_dotenv()


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
