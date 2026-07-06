"""
database/messages.py

Request messages repository.
"""

from typing import Optional

from .crud import (
    execute,
    fetch_one,
    fetch_all,
)


# -----------------------------
# Add Message
# -----------------------------
def add_message(
    tracking_code: str,
    sender_type: str,
    sender_id: int,
    message_type: str,
    message: str,
) -> int:
    """
    Save a request message.

    Returns:
        Message ID
    """

    return execute(
        """
        INSERT INTO request_messages
        (
            tracking_code,
            sender_type,
            sender_id,
            message_type,
            message
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            tracking_code,
            sender_type,
            sender_id,
            message_type,
            message,
        ),
    )


# -----------------------------
# Get Message
# -----------------------------
def get_message(
    message_id: int,
) -> Optional[dict]:

    row = fetch_one(
        """
        SELECT *
        FROM request_messages
        WHERE id = ?
        """,
        (message_id,),
    )

    return dict(row) if row else None


# -----------------------------
# Get Request Messages
# -----------------------------
def get_messages(
    tracking_code: str,
) -> list[dict]:

    rows = fetch_all(
        """
        SELECT *
        FROM request_messages
        WHERE tracking_code = ?
        ORDER BY created_at ASC, id ASC
        """,
        (tracking_code,),
    )

    return [dict(row) for row in rows]


# -----------------------------
# Last Message
# -----------------------------
def get_last_message(
    tracking_code: str,
) -> Optional[dict]:

    row = fetch_one(
        """
        SELECT *
        FROM request_messages
        WHERE tracking_code = ?
        ORDER BY created_at DESC, id DESC
        LIMIT 1
        """,
        (tracking_code,),
    )

    return dict(row) if row else None


# -----------------------------
# Delete Messages
# -----------------------------
def delete_messages(
    tracking_code: str,
) -> None:

    execute(
        """
        DELETE FROM request_messages
        WHERE tracking_code = ?
        """,
        (tracking_code,),
    )
