"""
database/crud.py

Generic CRUD helpers for Azarakhsh database.
"""

import sqlite3
from typing import Optional

from .connection import get_connection


# -----------------------------
# Execute
# -----------------------------
def execute(
    query: str,
    params: tuple = (),
) -> int:
    """
    Execute INSERT, UPDATE or DELETE query.

    Returns:
        lastrowid if available, otherwise 0.
    """

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(query, params)

        connection.commit()

        return cursor.lastrowid

    finally:

        connection.close()


# -----------------------------
# Fetch One
# -----------------------------
def fetch_one(
    query: str,
    params: tuple = (),
) -> Optional[sqlite3.Row]:
    """
    Execute SELECT and return one row.
    """

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(query, params)

        return cursor.fetchone()

    finally:

        connection.close()


# -----------------------------
# Fetch All
# -----------------------------
def fetch_all(
    query: str,
    params: tuple = (),
) -> list[sqlite3.Row]:
    """
    Execute SELECT and return all rows.
    """

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(query, params)

        return cursor.fetchall()

    finally:

        connection.close()


# -----------------------------
# Execute Many
# -----------------------------
def execute_many(
    query: str,
    params: list[tuple],
) -> None:
    """
    Execute query for multiple rows.
    """

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.executemany(query, params)

        connection.commit()

    finally:

        connection.close()


# -----------------------------
# Table Exists
# -----------------------------
def table_exists(table_name: str) -> bool:
    """
    Check whether a table exists.
    """

    row = fetch_one(
        """
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        AND name=?
        """,
        (table_name,),
    )

    return row is not None
