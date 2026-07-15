"""
database/crud.py

Generic CRUD helpers for PostgreSQL.
"""

from typing import Any

from .connection import get_connection


# -------------------------------------------------
# Execute
# -------------------------------------------------

def execute(
    query: str,
    params: tuple = (),
) -> int:
    """
    Execute INSERT / UPDATE / DELETE.

    Returns returned id if RETURNING exists.
    """

    connection = get_connection()

    try:

        with connection.cursor() as cursor:

            cursor.execute(
                query,
                params,
            )

            result = None

            if cursor.description:

                result = cursor.fetchone()

            connection.commit()

            if result:

                if isinstance(result, dict):

                    return next(
                        iter(result.values())
                    )

                return result[0]

            return 0

    finally:

        connection.close()



# -------------------------------------------------
# Fetch One
# -------------------------------------------------

def fetch_one(
    query: str,
    params: tuple = (),
) -> dict[str, Any] | None:
    """
    Return one row.
    """

    connection = get_connection()

    try:

        with connection.cursor() as cursor:

            cursor.execute(
                query,
                params,
            )

            row = cursor.fetchone()

            return row

    finally:

        connection.close()



# -------------------------------------------------
# Fetch All
# -------------------------------------------------

def fetch_all(
    query: str,
    params: tuple = (),
) -> list[dict[str, Any]]:
    """
    Return all rows.
    """

    connection = get_connection()

    try:

        with connection.cursor() as cursor:

            cursor.execute(
                query,
                params,
            )

            rows = cursor.fetchall()

            return rows

    finally:

        connection.close()



# -------------------------------------------------
# Execute Many
# -------------------------------------------------

def execute_many(
    query: str,
    params: list[tuple],
) -> None:
    """
    Execute many queries.
    """

    connection = get_connection()

    try:

        with connection.cursor() as cursor:

            cursor.executemany(
                query,
                params,
            )

            connection.commit()

    finally:

        connection.close()



# -------------------------------------------------
# Table Exists
# -------------------------------------------------

def table_exists(
    table_name: str,
) -> bool:
    """
    Check table existence.
    """

    row = fetch_one(
        """
        SELECT table_name

        FROM information_schema.tables

        WHERE table_schema='public'

        AND table_name=%s
        """,
        (
            table_name,
        ),
    )

    return row is not None



# -------------------------------------------------
# Column Exists
# -------------------------------------------------

def column_exists(
    table_name: str,
    column_name: str,
) -> bool:
    """
    Check column existence.
    """

    row = fetch_one(
        """
        SELECT column_name

        FROM information_schema.columns

        WHERE table_schema='public'

        AND table_name=%s

        AND column_name=%s
        """,
        (
            table_name,
            column_name,
        ),
    )

    return row is not None
