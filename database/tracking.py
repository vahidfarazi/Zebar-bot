"""
database/tracking.py

Tracking number database operations.
"""

from datetime import datetime

from .crud import fetch_one


# -----------------------------
# Last Tracking Number
# -----------------------------
def get_last_tracking_number() -> str | None:
    """
    Return last tracking code for current year.

    Example:
        SR-2026-0000001
    """

    year = datetime.now().year

    row = fetch_one(
        """
        SELECT tracking_code
        FROM requests
        WHERE tracking_code LIKE %s
        ORDER BY id DESC
        LIMIT 1
        """,
        (
            f"SR-{year}-%",
        ),
    )

    if not row:
        return None

    return row["tracking_code"]
