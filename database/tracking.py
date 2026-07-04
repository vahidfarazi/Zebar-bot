"""
database/tracking.py

Tracking number database operations.
"""

from .crud import fetch_one


# -----------------------------
# Get Last Tracking Number
# -----------------------------
def get_last_tracking_number(year: int) -> int:
    """
    Return the last issued tracking number for the given year.

    If no tracking exists, return 0.
    """

    row = fetch_one(
        """
        SELECT tracking_code
        FROM requests
        WHERE tracking_code LIKE ?
        ORDER BY tracking_code DESC
        LIMIT 1
        """,
        (f"SR-{year}-%",),
    )

    if row is None:
        return 0

    tracking_code = row["tracking_code"]

    try:
        return int(tracking_code.split("-")[-1])
    except (ValueError, IndexError):
        return 0
