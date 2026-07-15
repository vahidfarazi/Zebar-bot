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


# =================================================
# Create Request
# =================================================

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
            sub_service,
            status,
            priority,
            created_at,
            updated_at
        )

        VALUES
        (
            %s,
            %s,
            %s,
            %s,
            'OPEN',
            'NORMAL',
            CURRENT_TIMESTAMP,
            CURRENT_TIMESTAMP
        )

        RETURNING id
        """,
        (
            tracking_code,
            chat_id,
            service,
            sub_service,
        ),
    )



# =================================================
# Get By ID
# =================================================

def get_request(
    request_id: int,
) -> Optional[dict]:

    row = fetch_one(
        """
        SELECT *

        FROM requests

        WHERE id=%s
        """,
        (
            request_id,
        ),
    )

    return dict(row) if row else None



# =================================================
# Get By Tracking
# =================================================

def get_request_by_tracking(
    tracking_code: str,
) -> Optional[dict]:

    row = fetch_one(
        """
        SELECT *

        FROM requests

        WHERE tracking_code=%s
        """,
        (
            tracking_code,
        ),
    )

    return dict(row) if row else None



# Compatibility

def get_request_by_code(
    tracking_code: str,
) -> Optional[dict]:

    return get_request_by_tracking(
        tracking_code
    )



# =================================================
# Exists
# =================================================

def request_exists(
    tracking_code: str,
) -> bool:

    return (
        get_request_by_tracking(
            tracking_code
        )
        is not None
    )



# =================================================
# User Requests
# =================================================

def get_user_requests(
    chat_id: int,
) -> list[dict]:

    rows = fetch_all(
        """
        SELECT *

        FROM requests

        WHERE chat_id=%s

        ORDER BY id DESC
        """,
        (
            chat_id,
        ),
    )

    return [
        dict(row)
        for row in rows
    ]



# Alias

def get_requests(
) -> list[dict]:

    rows = fetch_all(
        """
        SELECT *

        FROM requests

        ORDER BY id DESC
        """
    )

    return [
        dict(row)
        for row in rows
    ]



# =================================================
# Expert Requests
# =================================================

def get_expert_requests(
    expert_id: int,
) -> list[dict]:

    rows = fetch_all(
        """
        SELECT *

        FROM requests

        WHERE expert_id=%s

        ORDER BY id DESC
        """,
        (
            expert_id,
        ),
    )

    return [
        dict(row)
        for row in rows
    ]



# =================================================
# Update Status
# =================================================

def update_request_status(
    request_id: int,
    status: str,
) -> None:

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



# =================================================
# Assign Expert
# =================================================

def assign_expert(
    request_id: int,
    expert_id: int,
) -> None:

    execute(
        """
        UPDATE requests

        SET

            expert_id=%s,

            assigned_at=CURRENT_TIMESTAMP,

            status='PENDING',

            updated_at=CURRENT_TIMESTAMP

        WHERE id=%s
        """,
        (
            expert_id,
            request_id,
        ),
    )



# =================================================
# Transfer Request
# =================================================

def transfer_request(
    request_id: int,
    new_expert_id: int,
) -> None:

    execute(
        """
        UPDATE requests

        SET

            expert_id=%s,

            transferred_at=CURRENT_TIMESTAMP,

            updated_at=CURRENT_TIMESTAMP

        WHERE id=%s
        """,
        (
            new_expert_id,
            request_id,
        ),
    )

# =================================================
# Save Expert Message
# =================================================

def save_expert_message(
    request_id: int,
    expert_chat_id: int,
    expert_message_id: int,
) -> None:

    execute(
        """
        UPDATE requests

        SET

            expert_chat_id=%s,

            expert_message_id=%s,

            first_response_at =
                COALESCE(
                    first_response_at,
                    CURRENT_TIMESTAMP
                ),

            updated_at=CURRENT_TIMESTAMP

        WHERE id=%s
        """,
        (
            expert_chat_id,
            expert_message_id,
            request_id,
        ),
    )



# =================================================
# Close Request
# =================================================

def close_request(
    request_id: int,
) -> None:

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



# =================================================
# Reopen Request
# =================================================

def reopen_request(
    request_id: int,
) -> None:

    execute(
        """
        UPDATE requests

        SET

            status='OPEN',

            closed_at=NULL,

            updated_at=CURRENT_TIMESTAMP

        WHERE id=%s
        """,
        (
            request_id,
        ),
    )



# =================================================
# Priority
# =================================================

def update_priority(
    request_id: int,
    priority: str,
) -> None:

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



# =================================================
# Delete Request
# =================================================

def delete_request(
    request_id: int,
) -> None:

    execute(
        """
        DELETE FROM requests

        WHERE id=%s
        """,
        (
            request_id,
        ),
    )



# =================================================
# Recent Requests
# =================================================

def get_recent_requests(
    limit: int = 20,
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



# =================================================
# Transferred Requests
# =================================================

def get_transferred_requests(
    limit: int = 50,
) -> list[dict]:

    rows = fetch_all(
        """
        SELECT *

        FROM requests

        WHERE transferred_at IS NOT NULL

        ORDER BY transferred_at DESC

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
# Counters
# =================================================

def _count_by_status(
    status: str,
) -> int:

    row = fetch_one(
        """
        SELECT COUNT(*) AS total

        FROM requests

        WHERE status=%s
        """,
        (
            status,
        ),
    )

    if not row:
        return 0

    return int(
        row["total"] or 0
    )



def count_requests() -> int:

    row = fetch_one(
        """
        SELECT COUNT(*) AS total

        FROM requests
        """
    )

    if not row:
        return 0

    return int(
        row["total"] or 0
    )



def count_open_requests() -> int:

    return _count_by_status(
        "OPEN"
    )



def count_pending_requests() -> int:

    return _count_by_status(
        "PENDING"
    )



def count_closed_requests() -> int:

    return _count_by_status(
        "CLOSED"
    )



def count_expert_requests(
    expert_id: int,
) -> int:

    row = fetch_one(
        """
        SELECT COUNT(*) AS total

        FROM requests

        WHERE expert_id=%s
        """,
        (
            expert_id,
        ),
    )

    if not row:
        return 0

    return int(
        row["total"] or 0
    )



# =================================================
# SLA Statistics
# =================================================

def get_sla_statistics() -> dict:

    row = fetch_one(
        """
        SELECT

            COUNT(*) AS total,

            AVG(
                EXTRACT(
                    EPOCH FROM
                    (
                        first_response_at
                        -
                        created_at
                    )
                ) / 60
            ) AS avg_response,

            AVG(
                EXTRACT(
                    EPOCH FROM
                    (
                        closed_at
                        -
                        created_at
                    )
                ) / 60
            ) AS avg_close

        FROM requests
        """
    )


    if not row:

        return {
            "total": 0,
            "avg_response": 0,
            "avg_close": 0,
        }


    return {

        "total":
            row["total"] or 0,

        "avg_response":
            round(
                row["avg_response"] or 0,
                2,
            ),

        "avg_close":
            round(
                row["avg_close"] or 0,
                2,
            ),

    }



# =================================================
# Summary
# =================================================

def get_requests_summary() -> dict:

    return {

        "total":
            count_requests(),

        "open":
            count_open_requests(),

        "pending":
            count_pending_requests(),

        "closed":
            count_closed_requests(),

    }
