"""
database/tracking.py

Tracking number database operations.
"""

from .crud import fetch_one


def get_last_tracking_number(year: int) -> int:
    """
    Return last tracking sequence for given year.
    """

    row = fetch_one(
        """
        SELECT tracking_code
        FROM requests
        WHERE tracking_code LIKE ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (f"SR-{year}-%",)
    )

    if not row:
        return 0

    tracking_code = row["tracking_code"]

    try:
        return int(tracking_code.split("-")[-1])
    except (ValueError, IndexError):
        return 0
