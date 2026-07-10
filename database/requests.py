"""
database/requests.py

Request repository.
"""

from typing import Optional

from .crud import (
    execute,
    fetch_one,
    fetch_all,
)


# -----------------------------
# Create Request
# -----------------------------
def insert_request(
    tracking_code: str,
    chat_id: int,
    service: str,
    sub_service: str | None = None,
) -> int:
    """
    Create new request.

    Returns:
        Request ID
    """

    return execute(
        """
        INSERT INTO requests
        (
            tracking_code,
            chat_id,
            service,
            sub_service
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            tracking_code,
            chat_id,
            service,
            sub_service,
        ),
    )


# -----------------------------
# Get By ID
# -----------------------------
def get_request(
    request_id: int,
) -> Optional[dict]:

    row = fetch_one(
        """
        SELECT *
        FROM requests
        WHERE id = ?
        """,
        (request_id,),
    )

    return dict(row) if row else None


# -----------------------------
# Get By Tracking
# -----------------------------
def get_request_by_tracking(
    tracking_code: str,
) -> Optional[dict]:

    row = fetch_one(
        """
        SELECT *
        FROM requests
        WHERE tracking_code = ?
        """,
        (tracking_code,),
    )

    return dict(row) if row else None


# -----------------------------
# Get User Requests
# -----------------------------
def get_user_requests(
    chat_id: int,
) -> list[dict]:

    rows = fetch_all(
        """
        SELECT *
        FROM requests
        WHERE chat_id = ?
        ORDER BY created_at DESC
        """,
        (chat_id,),
    )

    return [dict(row) for row in rows]


# -----------------------------
# Update Status
# -----------------------------
def update_request_status(
    request_id: int,
    status: str,
) -> None:

    execute(
        """
        UPDATE requests
        SET
            status = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (
            status,
            request_id,
        ),
    )


# -----------------------------
# Assign Expert
# -----------------------------
def assign_expert(
    request_id: int,
    expert_id: int,
) -> None:

    execute(
        """
        UPDATE requests
        SET
            expert_id = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (
            expert_id,
            request_id,
        ),
    )


# -----------------------------
# Save Expert Message
# -----------------------------
def save_expert_message(
    request_id: int,
    expert_chat_id: int,
    expert_message_id: int,
) -> None:

    execute(
        """
        UPDATE requests
        SET
            expert_chat_id = ?,
            expert_message_id = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (
            expert_chat_id,
            expert_message_id,
            request_id,
        ),
    )


# -----------------------------
# Close Request
# -----------------------------
def close_request(
    request_id: int,
) -> None:

    execute(
        """
        UPDATE requests
        SET
            status = 'CLOSED',
            closed_at = CURRENT_TIMESTAMP,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (request_id,),
    )


# -----------------------------
# Change Priority
# -----------------------------
def update_priority(
    request_id: int,
    priority: str,
) -> None:

    execute(
        """
        UPDATE requests
        SET
            priority = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (
            priority,
            request_id,
        ),
    )


# -----------------------------
# Delete Request
# -----------------------------
def delete_request(
    request_id: int,
) -> None:

    execute(
        """
        DELETE FROM requests
        WHERE id = ?
        """,
        (request_id,),
    )
    # -----------------------------
# Dashboard Statistics
# -----------------------------
def get_dashboard_statistics() -> dict:

    open_count = fetch_one(
        """
        SELECT COUNT(*) AS count
        FROM requests
        WHERE status = 'OPEN'
        """
    )["count"]

    closed_count = fetch_one(
        """
        SELECT COUNT(*) AS count
        FROM requests
        WHERE status = 'CLOSED'
        """
    )["count"]

    today_count = fetch_one(
        """
        SELECT COUNT(*) AS count
        FROM requests
        WHERE DATE(created_at)=DATE('now','localtime')
        """
    )["count"]

    expert_count = fetch_one(
        """
        SELECT COUNT(*) AS count
        FROM experts
        WHERE is_active = 1
        """
    )["count"]

    return {

        "open": open_count,

        "closed": closed_count,

        "today": today_count,

        "experts": expert_count,

    }


# -----------------------------
# Recent Requests
# -----------------------------
def get_recent_requests(
    limit: int = 20,
) -> list[dict]:

    rows = fetch_all(
        """
        SELECT *

        FROM requests

        ORDER BY id DESC

        LIMIT ?
        """,
        (limit,),
    )

    return [

        dict(row)

        for row in rows

    ]
