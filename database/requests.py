"""
database/requests.py

Advanced request repository.
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
    """
    Create new request.
    """

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
    """
    Return request by id.
    """

    row = fetch_one(
        """
        SELECT *

        FROM requests

        WHERE id = %s
        """,
        (
            request_id,
        ),
    )

    return dict(row) if row else None


# =================================================
# Get By Tracking Code
# =================================================

def get_request_by_tracking(
    tracking_code: str,
) -> Optional[dict]:
    """
    Return request by tracking code.
    """

    row = fetch_one(
        """
        SELECT *

        FROM requests

        WHERE tracking_code = %s
        """,
        (
            tracking_code,
        ),
    )

    return dict(row) if row else None

# =================================================
# Exists
# =================================================

def request_exists(
    tracking_code: str,
) -> bool:
    """
    Check whether request exists.
    """

    return (
        get_request_by_tracking(
            tracking_code,
        )
        is not None
    )


# =================================================
# User Requests
# =================================================

def get_user_requests(
    chat_id: int,
) -> list[dict]:
    """
    Return all requests of user.
    """

    rows = fetch_all(
        """
        SELECT *

        FROM requests

        WHERE chat_id = %s

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


# =================================================
# Expert Requests
# =================================================

def get_expert_requests(
    expert_id: int,
) -> list[dict]:
    """
    Return expert requests.
    """

    rows = fetch_all(
        """
        SELECT *

        FROM requests

        WHERE expert_id = %s

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
# Recent Requests
# =================================================

def get_recent_requests(
    limit: int = 20,
) -> list[dict]:
    """
    Return latest requests.
    """

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
# Update Status
# =================================================

def update_request_status(
    request_id: int,
    status: str,
) -> None:
    """
    Update request status.
    """

    execute(
        """
        UPDATE requests

        SET

            status = %s,

            updated_at = CURRENT_TIMESTAMP

        WHERE id = %s
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
    """
    Assign request to expert.
    """

    execute(
        """
        UPDATE requests

        SET

            expert_id = %s,

            assigned_at = CURRENT_TIMESTAMP,

            status = 'PENDING',

            updated_at = CURRENT_TIMESTAMP

        WHERE id = %s
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
    """
    Transfer request to another expert.
    """

    execute(
        """
        UPDATE requests

        SET

            expert_id = %s,

            transferred_at = CURRENT_TIMESTAMP,

            updated_at = CURRENT_TIMESTAMP

        WHERE id = %s
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
    """
    Save forwarded expert message ids.
    """

    execute(
        """
        UPDATE requests

        SET

            expert_chat_id = %s,

            expert_message_id = %s,

            first_response_at =
                COALESCE(
                    first_response_at,
                    CURRENT_TIMESTAMP
                ),

            updated_at = CURRENT_TIMESTAMP

        WHERE id = %s
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
    """
    Close request.
    """

    execute(
        """
        UPDATE requests

        SET

            status = 'CLOSED',

            closed_at = CURRENT_TIMESTAMP,

            updated_at = CURRENT_TIMESTAMP

        WHERE id = %s
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
    """
    Reopen closed request.
    """

    execute(
        """
        UPDATE requests

        SET

            status = 'OPEN',

            closed_at = NULL,

            updated_at = CURRENT_TIMESTAMP

        WHERE id = %s
        """,
        (
            request_id,
        ),
    )


# =================================================
# Update Priority
# =================================================

def update_priority(
    request_id: int,
    priority: str,
) -> None:
    """
    Update request priority.
    """

    execute(
        """
        UPDATE requests

        SET

            priority = %s,

            updated_at = CURRENT_TIMESTAMP

        WHERE id = %s
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
    """
    Delete request permanently.
    """

    execute(
        """
        DELETE FROM requests

        WHERE id = %s
        """,
        (
            request_id,
        ),
    )

# =================================================
# Count Requests
# =================================================

def count_requests() -> int:
    """
    Return total requests.
    """

    row = fetch_one(
        """
        SELECT COUNT(*) AS total

        FROM requests
        """
    )

    return int(row["total"] or 0)


# =================================================
# Count Open Requests
# =================================================

def count_open_requests() -> int:
    """
    Return total open requests.
    """

    row = fetch_one(
        """
        SELECT COUNT(*) AS total

        FROM requests

        WHERE status = 'OPEN'
        """
    )

    return int(row["total"] or 0)


# =================================================
# Count Pending Requests
# =================================================

def count_pending_requests() -> int:
    """
    Return total pending requests.
    """

    row = fetch_one(
        """
        SELECT COUNT(*) AS total

        FROM requests

        WHERE status = 'PENDING'
        """
    )

    return int(row["total"] or 0)


# =================================================
# Count Closed Requests
# =================================================

def count_closed_requests() -> int:
    """
    Return total closed requests.
    """

    row = fetch_one(
        """
        SELECT COUNT(*) AS total

        FROM requests

        WHERE status = 'CLOSED'
        """
    )

    return int(row["total"] or 0)


# =================================================
# Count Expert Requests
# =================================================

def count_expert_requests(
    expert_id: int,
) -> int:
    """
    Return total requests assigned to an expert.
    """

    row = fetch_one(
        """
        SELECT COUNT(*) AS total

        FROM requests

        WHERE expert_id = %s
        """,
        (
            expert_id,
        ),
    )

    return int(row["total"] or 0)

# =================================================
# Transferred Requests
# =================================================

def get_transferred_requests(
    limit: int = 50,
) -> list[dict]:
    """
    Return transferred requests.
    """

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
# SLA Statistics
# =================================================

def get_sla_statistics() -> dict:
    """
    SLA response statistics.
    """

    row = fetch_one(
        """
        SELECT

            COUNT(*) AS total,

            AVG(
                EXTRACT(
                    EPOCH FROM
                    (
                        first_response_at - created_at
                    )
                ) / 60
            ) AS avg_response,

            AVG(
                EXTRACT(
                    EPOCH FROM
                    (
                        closed_at - created_at
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
            row.get("total", 0) or 0,

        "avg_response":
            round(
                row.get("avg_response", 0) or 0,
                2,
            ),

        "avg_close":
            round(
                row.get("avg_close", 0) or 0,
                2,
            ),
    }


# =================================================
# Requests Summary
# =================================================

def get_requests_summary() -> dict:
    """
    Return request counters.
    """

    return {
        "total": count_requests(),
        "open": count_open_requests(),
        "pending": count_pending_requests(),
        "closed": count_closed_requests(),
    }
