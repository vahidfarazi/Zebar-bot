"""
database/tracking.py
"""

from .crud import fetch_one


def get_next_tracking_number() -> int:
    """
    آخرین شماره استفاده‌شده را از جدول requests می‌خواند
    و شماره بعدی را برمی‌گرداند.
    """

    row = fetch_one(
        """
        SELECT
            MAX(
                CAST(RIGHT(tracking_code, 7) AS INTEGER)
            ) AS max_number
        FROM requests
        WHERE tracking_code LIKE '140511%'
        """
    )

    if row is None:
        return 1

    if row["max_number"] is None:
        return 1

    return row["max_number"] + 1


def generate_tracking_code() -> str:
    """
    فقط برای سازگاری
    """

    number = get_next_tracking_number()

    return f"140511{number:07d}"
