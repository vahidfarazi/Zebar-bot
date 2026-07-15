"""
database/history.py

Request history repository.
"""

from .crud import (
    execute,
    fetch_all,
    fetch_one,
)


# =================================================
# Add History
# =================================================

def add_history(
    tracking_code: str,
    event_type: str,
    actor_type: str,
    actor_id: int | None = None,
    description: str = "",
) -> None:
    """
    Add history event.
    """

    execute(
        """
        INSERT INTO request_history
        (
            tracking_code,
            event_type,
            actor_type,
            actor_id,
            description,
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
            event_type,
            actor_type,
            actor_id,
            description,
        ),
    )



# =================================================
# Get History Timeline
# =================================================

def get_history(
    tracking_code: str,
) -> list[dict]:
    """
    Return request timeline.
    """

    rows = fetch_all(
        """
        SELECT *

        FROM request_history

        WHERE tracking_code=%s

        ORDER BY created_at ASC, id ASC
        """,
        (
            tracking_code,
        ),
    )

    return [
        dict(row)
        for row in rows
    ]



# Compatibility Alias

def get_request_history(
    tracking_code: str,
) -> list[dict]:

    return get_history(
        tracking_code
    )



# =================================================
# Latest Event
# =================================================

def get_latest_history(
    tracking_code: str,
) -> dict | None:

    row = fetch_one(
        """
        SELECT *

        FROM request_history

        WHERE tracking_code=%s

        ORDER BY id DESC

        LIMIT 1
        """,
        (
            tracking_code,
        ),
    )

    return dict(row) if row else None



# =================================================
# Count History
# =================================================

def count_history(
    tracking_code: str,
) -> int:

    row = fetch_one(
        """
        SELECT COUNT(*) AS total

        FROM request_history

        WHERE tracking_code=%s
        """,
        (
            tracking_code,
        ),
    )

    if not row:
        return 0

    return int(
        row["total"] or 0
    )



# =================================================
# Transfer
# =================================================

def add_transfer_history(
    tracking_code: str,
    from_expert: int | None,
    to_expert: int,
    admin_id: int,
) -> None:

    add_history(
        tracking_code,
        "REQUEST_TRANSFER",
        "ADMIN",
        admin_id,
        (
            f"انتقال درخواست از کارشناس "
            f"{from_expert or 'بدون تخصیص'} "
            f"به کارشناس {to_expert}"
        ),
    )



# =================================================
# Status Change
# =================================================

def add_status_history(
    tracking_code: str,
    old_status: str,
    new_status: str,
    actor_id: int,
    actor_type: str,
) -> None:

    add_history(
        tracking_code,
        "STATUS_CHANGE",
        actor_type,
        actor_id,
        (
            f"تغییر وضعیت از "
            f"{old_status} "
            f"به "
            f"{new_status}"
        ),
    )



# =================================================
# Expert Assignment
# =================================================

def add_assignment_history(
    tracking_code: str,
    expert_id: int,
    actor_id: int,
) -> None:

    add_history(
        tracking_code,
        "EXPERT_ASSIGNED",
        "ADMIN",
        actor_id,
        (
            f"تخصیص درخواست به کارشناس "
            f"{expert_id}"
        ),
    )



# =================================================
# Admin Action
# =================================================

def add_admin_history(
    tracking_code: str,
    admin_id: int,
    action: str,
    description: str = "",
) -> None:

    add_history(
        tracking_code,
        action,
        "ADMIN",
        admin_id,
        description,
    )



# =================================================
# Expert Action
# =================================================

def add_expert_history(
    tracking_code: str,
    expert_id: int,
    action: str,
    description: str = "",
) -> None:

    add_history(
        tracking_code,
        action,
        "EXPERT",
        expert_id,
        description,
    )



# =================================================
# Delete History
# =================================================

def delete_history(
    tracking_code: str,
) -> None:

    execute(
        """
        DELETE FROM request_history

        WHERE tracking_code=%s
        """,
        (
            tracking_code,
        ),
    )
