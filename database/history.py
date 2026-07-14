"""
database/history.py

Request history repository.
"""

from .crud import (
    execute,
    fetch_all,
    fetch_one,
)


# -------------------------------------------------
# Add History
# -------------------------------------------------
def add_history(
    tracking_code: str,
    event_type: str,
    actor_type: str,
    actor_id: int | None = None,
    description: str = "",
) -> None:

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
        (%s,%s,%s,%s,%s)
        """,
        (
            tracking_code,
            event_type,
            actor_type,
            actor_id,
            description,
        ),
    )


# -------------------------------------------------
# Get History
# -------------------------------------------------
def get_history(
    tracking_code: str,
) -> list[dict]:

    rows = fetch_all(
        """
        SELECT *

        FROM request_history

        WHERE tracking_code=%s

        ORDER BY id ASC
        """,
        (
            tracking_code,
        ),
    )

    return [
        dict(row)
        for row in rows
    ]


# -------------------------------------------------
# Add Transfer History
# -------------------------------------------------
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


# -------------------------------------------------
# Add Status Change
# -------------------------------------------------
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


# -------------------------------------------------
# Add Expert Assignment
# -------------------------------------------------
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


# -------------------------------------------------
# Get Latest Event
# -------------------------------------------------
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


# -------------------------------------------------
# Delete History
# -------------------------------------------------
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
