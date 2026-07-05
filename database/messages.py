"""
database/messages.py

Request messages CRUD.
"""

from .crud import (
    execute,
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
) -> None:

    execute(
        """
        INSERT INTO request_messages (

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
# Get Messages
# -----------------------------
def get_messages(
    tracking_code: str,
):

    return fetch_all(

        """
        SELECT *

        FROM request_messages

        WHERE tracking_code=?

        ORDER BY id
        """,

        (
            tracking_code,
        ),

    )


# -----------------------------
# Last Message
# -----------------------------
def get_last_message(
    tracking_code: str,
):

    rows = fetch_all(

        """
        SELECT *

        FROM request_messages

        WHERE tracking_code=?

        ORDER BY id DESC

        LIMIT 1
        """,

        (
            tracking_code,
        ),

    )

    if rows:

        return rows[0]

    return None
