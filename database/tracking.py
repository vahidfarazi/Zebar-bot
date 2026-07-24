"""
database/tracking.py

Tracking number generator.
"""

from .crud import fetch_one


# =================================================
# Get Next Tracking Number
# =================================================

def get_next_tracking_number() -> int:
    """
    آخرین شماره ثبت‌شده را از جدول requests پیدا می‌کند
    و شماره بعدی را برمی‌گرداند.

    Format:
        1405110000001
    """

    row = fetch_one(
        """
        SELECT
            MAX(
                CAST(
                    RIGHT(tracking_code, 7)
                    AS INTEGER
                )
            ) AS max_number

        FROM requests

        WHERE tracking_code LIKE %s
        """,
        (
            "140511%",
        ),
    )


    if not row:
        return 1


    max_number = row.get(
        "max_number"
    )


    if max_number is None:
        return 1


    return max_number + 1



# =================================================
# Generate Tracking Code
# =================================================

def generate_tracking_code() -> str:
    """
    ساخت کد پیگیری جدید.

    Example:
        1405110000011
    """

    number = get_next_tracking_number()

    return (
        f"140511"
        f"{number:07d}"
    )
