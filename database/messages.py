"""
database/messages.py

Advanced request messages repository.
"""

from typing import Optional

from .crud import (
    execute,
    fetch_one,
    fetch_all,
)


# =================================================
# Add Message
# =================================================

def add_message(
    tracking_code: str,
    sender_type: str,
    sender_id: int,
    message_type: str,
    message: str,
) -> int:

    return execute(
        """
        INSERT INTO request_messages
        (
            tracking_code,
            sender_type,
            sender_id,
            message_type,
            message,
            created_at
        )

        VALUES
        (
            %s,
            %s,
            %s,
            %s,
            %s,
            CURRENT_TIMESTAMP
        )
        """,
        (
            tracking_code,
            sender_type,
            sender_id,
            message_type,
            message,
        ),
    )


# =================================================
# Get Message
# =================================================

def get_message(
    message_id: int,
) -> Optional[dict]:

    row = fetch_one(
        """
        SELECT *

        FROM request_messages

        WHERE id=%s
        """,
        (
            message_id,
        ),
    )

    return dict(row) if row else None


# =================================================
# Request Messages
# =================================================

def get_messages(
    tracking_code: str,
) -> list[dict]:

    rows = fetch_all(
        """
        SELECT *

        FROM request_messages

        WHERE tracking_code=%s

        ORDER BY created_at ASC,id ASC
        """,
        (
            tracking_code,
        ),
    )

    return [
        dict(row)
        for row in rows
    ]


# =================================================
# Last Message
# =================================================

def get_last_message(
    tracking_code: str,
) -> Optional[dict]:

    row = fetch_one(
        """
        SELECT *

        FROM request_messages

        WHERE tracking_code=%s

        ORDER BY created_at DESC,id DESC

        LIMIT 1
        """,
        (
            tracking_code,
        ),
    )

    return dict(row) if row else None


# =================================================
# Last User Message
# =================================================

def get_last_user_message(
    tracking_code: str,
) -> Optional[dict]:

    row = fetch_one(
        """
        SELECT *

        FROM request_messages

        WHERE tracking_code=%s

        AND sender_type='USER'

        ORDER BY created_at DESC,id DESC

        LIMIT 1
        """,
        (
            tracking_code,
        ),
    )

    return dict(row) if row else None


# =================================================
# Last Expert Message
# =================================================

def get_last_expert_message(
    tracking_code: str,
) -> Optional[dict]:

    row = fetch_one(
        """
        SELECT *

        FROM request_messages

        WHERE tracking_code=%s

        AND sender_type='EXPERT'

        ORDER BY created_at DESC,id DESC

        LIMIT 1
        """,
        (
            tracking_code,
        ),
    )

    return dict(row) if row else None


# =================================================
# Count Messages
# =================================================

def count_messages(
    tracking_code: str,
) -> int:

    row = fetch_one(
        """
        SELECT COUNT(*) AS total

        FROM request_messages

        WHERE tracking_code=%s
        """,
        (
            tracking_code,
        ),
    )

    return row["total"] or 0


# =================================================
# Expert Messages
# =================================================

def get_expert_messages(
    tracking_code: str,
) -> list[dict]:

    rows = fetch_all(
        """
        SELECT *

        FROM request_messages

        WHERE tracking_code=%s

        AND sender_type='EXPERT'

        ORDER BY created_at ASC
        """,
        (
            tracking_code,
        ),
    )

    return [
        dict(row)
        for row in rows
    ]


# =================================================
# User Messages
# =================================================

def get_user_messages(
    tracking_code: str,
) -> list[dict]:

    rows = fetch_all(
        """
        SELECT *

        FROM request_messages

        WHERE tracking_code=%s

        AND sender_type='USER'

        ORDER BY created_at ASC
        """,
        (
            tracking_code,
        ),
    )

    return [
        dict(row)
        for row in rows
    ]


# =================================================
# Expert Message Statistics
# =================================================

def get_expert_message_statistics() -> list[dict]:

    rows = fetch_all(
        """
        SELECT

        sender_id AS expert_id,

        COUNT(*) AS messages

        FROM request_messages

        WHERE sender_type='EXPERT'

        GROUP BY sender_id

        ORDER BY messages DESC
        """
    )

    return [
        {
            "expert_id": row["expert_id"],
            "messages": row["messages"] or 0,
        }
        for row in rows
    ]


# =================================================
# Delete Messages
# =================================================

def delete_messages(
    tracking_code: str,
) -> None:

    execute(
        """
        DELETE FROM request_messages

        WHERE tracking_code=%s
        """,
        (
            tracking_code,
        ),
    )
