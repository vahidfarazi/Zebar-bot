"""
database/crud.py

Generic CRUD helpers for PostgreSQL.
"""

from typing import Any

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

    Returns inserted id if RETURNING is used,
    otherwise 0.
    """

    connection = get_connection()

    try:

        with connection.cursor() as cursor:

            cursor.execute(query, params)

            result = None

            if cursor.description:
                result = cursor.fetchone()

            connection.commit()

            if result:

                return list(result.values())[0]

            return 0

    finally:

        connection.close()


# -----------------------------
# Fetch One
# -----------------------------
def fetch_one(
    query: str,
    params: tuple = (),
) -> dict[str, Any] | None:
    """
    Execute SELECT and return one row.
    """

    connection = get_connection()

    try:

        with connection.cursor() as cursor:

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
) -> list[dict[str, Any]]:
    """
    Execute SELECT and return all rows.
    """

    connection = get_connection()

    try:

        with connection.cursor() as cursor:

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

        with connection.cursor() as cursor:

            cursor.executemany(query, params)

            connection.commit()

    finally:

        connection.close()


# -----------------------------
# Table Exists
# -----------------------------
def table_exists(
    table_name: str,
) -> bool:
    """
    Check whether a table exists.
    """

    row = fetch_one(
        """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema='public'
        AND table_name=%s
        """,
        (table_name,),
    )

    return row is not None
