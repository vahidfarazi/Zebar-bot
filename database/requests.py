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


# -------------------------------------------------
# Create Request
# -------------------------------------------------
def insert_request(
    tracking_code: str,
    chat_id: int,
    service: str,
    sub_service: str | None = None,
) -> int:

    return execute(
        """
        INSERT INTO requests
        (
            tracking_code,
            chat_id,
            service,
            sub_service
        )
        VALUES (%s,%s,%s,%s)
        """,
        (
            tracking_code,
            chat_id,
            service,
            sub_service,
        ),
    )


# -------------------------------------------------
# Get Request By ID
# -------------------------------------------------
def get_request(
    request_id: int,
) -> Optional[dict]:

    row = fetch_one(
        """
        SELECT *
        FROM requests
        WHERE id=%s
        """,
        (request_id,),
    )

    return dict(row) if row else None


# -------------------------------------------------
# Get By Tracking
# -------------------------------------------------
def get_request_by_tracking(
    tracking_code: str,
) -> Optional[dict]:

    row = fetch_one(
        """
        SELECT *
        FROM requests
        WHERE tracking_code=%s
        """,
        (tracking_code,),
    )

    return dict(row) if row else None


# -------------------------------------------------
# User Requests
# -------------------------------------------------
def get_user_requests(
    chat_id:int,
) -> list[dict]:

    rows = fetch_all(
        """
        SELECT *
        FROM requests
        WHERE chat_id=%s
        ORDER BY created_at DESC
        """,
        (chat_id,),
    )

    return [
        dict(row)
        for row in rows
    ]


# -------------------------------------------------
# Update Status
# -------------------------------------------------
def update_request_status(
    request_id:int,
    status:str,
):

    execute(
        """
        UPDATE requests

        SET
        status=%s,
        updated_at=CURRENT_TIMESTAMP

        WHERE id=%s
        """,
        (
            status,
            request_id,
        ),
    )


# -------------------------------------------------
# Assign Expert
# -------------------------------------------------
def assign_expert(
    request_id:int,
    expert_id:int,
):

    execute(
        """
        UPDATE requests

        SET
        expert_id=%s,
        updated_at=CURRENT_TIMESTAMP

        WHERE id=%s
        """,
        (
            expert_id,
            request_id,
        ),
    )


# -------------------------------------------------
# Transfer Request
# -------------------------------------------------
def transfer_request(
    request_id:int,
    new_expert_id:int,
):

    execute(
        """
        UPDATE requests

        SET

        expert_id=%s,

        updated_at=CURRENT_TIMESTAMP

        WHERE id=%s
        """,
        (
            new_expert_id,
            request_id,
        ),
    )


# -------------------------------------------------
# Get Transferred Requests
# -------------------------------------------------
def get_transferred_requests(
    limit:int=50,
) -> list[dict]:

    rows = fetch_all(
        """
        SELECT *

        FROM requests

        WHERE expert_id IS NOT NULL

        AND updated_at <> created_at

        ORDER BY updated_at DESC

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


# -------------------------------------------------
# Expert Requests
# -------------------------------------------------
def get_expert_requests(
    expert_id:int,
) -> list[dict]:

    rows = fetch_all(
        """
        SELECT *

        FROM requests

        WHERE expert_id=%s

        ORDER BY created_at DESC
        """,
        (
            expert_id,
        ),
    )

    return [
        dict(row)
        for row in rows
    ]


# -------------------------------------------------
# Save Expert Message
# -------------------------------------------------
def save_expert_message(
    request_id:int,
    expert_chat_id:int,
    expert_message_id:int,
):

    execute(
        """
        UPDATE requests

        SET

        expert_chat_id=%s,

        expert_message_id=%s,

        updated_at=CURRENT_TIMESTAMP

        WHERE id=%s
        """,
        (
            expert_chat_id,
            expert_message_id,
            request_id,
        ),
    )


# -------------------------------------------------
# Close Request
# -------------------------------------------------
def close_request(
    request_id:int,
):

    execute(
        """
        UPDATE requests

        SET

        status='CLOSED',

        closed_at=CURRENT_TIMESTAMP,

        updated_at=CURRENT_TIMESTAMP

        WHERE id=%s
        """,
        (
            request_id,
        ),
    )


# -------------------------------------------------
# Priority
# -------------------------------------------------
def update_priority(
    request_id:int,
    priority:str,
):

    execute(
        """
        UPDATE requests

        SET

        priority=%s,

        updated_at=CURRENT_TIMESTAMP

        WHERE id=%s
        """,
        (
            priority,
            request_id,
        ),
    )


# -------------------------------------------------
# Recent Requests
# -------------------------------------------------
def get_recent_requests(
    limit:int=20,
) -> list[dict]:

    rows = fetch_all(
        """
        SELECT *

        FROM requests

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
