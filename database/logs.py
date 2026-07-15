"""
database/logs.py

System logs repository.
"""

from .crud import (
    execute,
    fetch_one,
    fetch_all,
)


# =================================================
# Insert Log
# =================================================

def insert_log(
    level: str,
    module: str,
    action: str,
    description: str,
) -> None:
    """
    Insert system log.
    """

    execute(
        """
        INSERT INTO system_logs
        (
            level,
            module,
            action,
            description,
            created_at
        )

        VALUES
        (
            %s,
            %s,
            %s,
            %s,
            CURRENT_TIMESTAMP
        )
        """,
        (
            level,
            module,
            action,
            description,
        ),
    )



# =================================================
# Get Log
# =================================================

def get_log(
    log_id: int,
) -> dict | None:
    """
    Return single log.
    """

    row = fetch_one(
        """
        SELECT *

        FROM system_logs

        WHERE id=%s
        """,
        (
            log_id,
        ),
    )

    return dict(row) if row else None



# =================================================
# Get Logs
# =================================================

def get_logs(
    level: str | None = None,
    limit: int = 100,
) -> list[dict]:
    """
    Return logs.
    """

    if level:

        rows = fetch_all(
            """
            SELECT *

            FROM system_logs

            WHERE level=%s

            ORDER BY id DESC

            LIMIT %s
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

            LIMIT %s
            """,
            (
                limit,
            ),
        )

    return [
        dict(row)
        for row in rows
    ]



# =================================================
# Latest Log
# =================================================

def get_latest_log() -> dict | None:

    row = fetch_one(
        """
        SELECT *

        FROM system_logs

        ORDER BY id DESC

        LIMIT 1
        """
    )

    return dict(row) if row else None



# =================================================
# Count Logs
# =================================================

def count_logs(
    level: str | None = None,
) -> int:

    if level:

        row = fetch_one(
            """
            SELECT COUNT(*) AS total

            FROM system_logs

            WHERE level=%s
            """,
            (
                level,
            ),
        )

    else:

        row = fetch_one(
            """
            SELECT COUNT(*) AS total

            FROM system_logs
            """
        )

    return int(
        row["total"] or 0
    )



# =================================================
# Delete Logs
# =================================================

def clear_logs() -> None:
    """
    Delete all logs.
    """

    execute(
        """
        DELETE FROM system_logs
        """
    )



# =================================================
# Compatibility
# =================================================

def delete_logs() -> None:

    clear_logs()
