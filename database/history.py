"""
database/history.py

Request history repository.
"""

from .crud import execute, fetch_all


# -----------------------------
# Add History
# -----------------------------
def add_history(
    tracking_code: str,
    event_type: str,
    actor_type: str,
    actor_id: int | None = None,
    description: str = "",
) -> None:
    """
    Register a request event.
    """

    execute(
        """
        INSERT INTO request_history
        (
            tracking_code,
            event_type,
            actor_type,
            actor_id,
            description
        )
        VALUES
        (%s, %s, %s, %s, %s)
        """,
        (
            tracking_code,
            event_type,
            actor_type,
            actor_id,
            description,
        ),
    )


# -----------------------------
# Get History
# -----------------------------
def get_history(
    tracking_code: str,
) -> list[dict]:
    """
    Return request history.
    """

    rows = fetch_all(
        """
        SELECT *
        FROM request_history
        WHERE tracking_code = %s
        ORDER BY id
        """,
        (
            tracking_code,
        ),
    )

    return [
        dict(row)
        for row in rows
    ]


# -----------------------------
# Delete History
# -----------------------------
def delete_history(
    tracking_code: str,
) -> None:
    """
    Delete request history.
    """

    execute(
        """
        DELETE FROM request_history
        WHERE tracking_code = %s
        """,
        (
            tracking_code,
        ),
    )
