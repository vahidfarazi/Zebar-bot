"""
database/logs.py

System log repository.
"""

from .crud import execute, fetch_all


# -----------------------------
# Insert Log
# -----------------------------
def insert_log(
    level: str,
    module: str,
    action: str,
    description: str,
) -> None:
    """
    Insert a log entry.
    """

    execute(
        """
        INSERT INTO system_logs
        (
            level,
            module,
            action,
            description
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            level,
            module,
            action,
            description,
        ),
    )


# -----------------------------
# Get Logs
# -----------------------------
def get_logs(
    level: str | None = None,
    limit: int = 100,
) -> list[dict]:
    """
    Return latest logs.
    """

    if level:

        rows = fetch_all(
            """
            SELECT *
            FROM system_logs
            WHERE level = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (
                level,
                limit,
            ),
        )

    else:

        rows = fetch_all(
            """
            SELECT *
            FROM system_logs
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        )

    return [dict(row) for row in rows]


# -----------------------------
# Clear Logs
# -----------------------------
def clear_logs() -> None:
    """
    Delete all log records.
    """

    execute(
        """
        DELETE FROM system_logs
        """
    )
