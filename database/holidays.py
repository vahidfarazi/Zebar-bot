"""
database/holidays.py

Holiday repository.
"""

from .crud import execute, fetch_one, fetch_all


# -----------------------------
# Add Holiday
# -----------------------------
def add_holiday(
    holiday_date: str,
) -> None:
    """
    Add holiday.
    """

    execute(
        """
        INSERT OR IGNORE INTO holidays
        (
            holiday_date,
            enabled
        )
        VALUES (?, 1)
        """,
        (holiday_date,),
    )


# -----------------------------
# Remove Holiday
# -----------------------------
def remove_holiday(
    holiday_date: str,
) -> None:
    """
    Remove holiday.
    """

    execute(
        """
        DELETE FROM holidays
        WHERE holiday_date = ?
        """,
        (holiday_date,),
    )


# -----------------------------
# Enable Holiday
# -----------------------------
def enable_holiday(
    holiday_date: str,
) -> None:
    """
    Enable holiday.
    """

    execute(
        """
        UPDATE holidays
        SET enabled = 1
        WHERE holiday_date = ?
        """,
        (holiday_date,),
    )


# -----------------------------
# Disable Holiday
# -----------------------------
def disable_holiday(
    holiday_date: str,
) -> None:
    """
    Disable holiday.
    """

    execute(
        """
        UPDATE holidays
        SET enabled = 0
        WHERE holiday_date = ?
        """,
        (holiday_date,),
    )


# -----------------------------
# Is Holiday
# -----------------------------
def is_holiday(
    holiday_date: str,
) -> bool:
    """
    Check whether a date is an enabled holiday.
    """

    row = fetch_one(
        """
        SELECT holiday_date
        FROM holidays
        WHERE holiday_date = ?
        AND enabled = 1
        """,
        (holiday_date,),
    )

    return row is not None


# -----------------------------
# Get All Holidays
# -----------------------------
def get_all_holidays() -> list[dict]:
    """
    Return all holidays.
    """

    rows = fetch_all(
        """
        SELECT *
        FROM holidays
        ORDER BY holiday_date
        """
    )

    return [dict(row) for row in rows]
