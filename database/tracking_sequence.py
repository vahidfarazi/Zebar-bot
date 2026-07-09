"""
database/tracking_sequence.py

Tracking sequence manager.
"""

from datetime import datetime

from .crud import (
    fetch_one,
    execute,
)


# ----------------------------------------
# Department Codes
# ----------------------------------------
DEPARTMENT_CODES = {
    "CUSTOMER_SERVICE": "11",
    "SAFETY": "22",
    "ENGINEERING": "33",
}


# ----------------------------------------
# Jalali Year
# ----------------------------------------
def get_current_year() -> str:
    """
    فعلاً سال شمسی ثابت.
    بعداً به jdatetime تبدیل می‌شود.
    """

    return "1405"


# ----------------------------------------
# Next Tracking Number
# ----------------------------------------
def get_next_tracking_code(
    department_code: str = "11",
) -> str:

    year = get_current_year()

    row = fetch_one(
        """
        SELECT last_number
        FROM tracking_sequences
        WHERE year = ?
        AND department_code = ?
        """,
        (
            year,
            department_code,
        ),
    )

    if row is None:

        last_number = 1

        execute(
            """
            INSERT INTO tracking_sequences
            (
                year,
                department_code,
                last_number
            )
            VALUES (?, ?, ?)
            """,
            (
                year,
                department_code,
                last_number,
            ),
        )

    else:

        last_number = row["last_number"] + 1

        execute(
            """
            UPDATE tracking_sequences
            SET last_number = ?
            WHERE year = ?
            AND department_code = ?
            """,
            (
                last_number,
                year,
                department_code,
            ),
        )

    return f"{year}{department_code}{last_number:07d}"
