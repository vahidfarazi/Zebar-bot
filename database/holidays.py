"""
database/holidays.py

Holiday repository.
"""

from .crud import (
    execute,
    fetch_one,
    fetch_all,
)


# =================================================
# Add Holiday
# =================================================

def add_holiday(
    holiday_date: str,
) -> None:

    execute(
        """
        INSERT INTO holidays
        (
            holiday_date,
            enabled
        )

        VALUES
        (
            %s,
            TRUE
        )

        ON CONFLICT(holiday_date)

        DO UPDATE SET

            enabled=TRUE
        """,
        (
            holiday_date,
        ),
    )



# =================================================
# Get Holiday
# =================================================

def get_holiday(
    holiday_date: str,
) -> dict | None:

    row = fetch_one(
        """
        SELECT *

        FROM holidays

        WHERE holiday_date=%s
        """,
        (
            holiday_date,
        ),
    )

    return dict(row) if row else None



# =================================================
# Exists
# =================================================

def holiday_exists(
    holiday_date: str,
) -> bool:

    return get_holiday(
        holiday_date
    ) is not None



# =================================================
# Remove Holiday
# =================================================

def remove_holiday(
    holiday_date: str,
) -> None:

    execute(
        """
        DELETE FROM holidays

        WHERE holiday_date=%s
        """,
        (
            holiday_date,
        ),
    )



# =================================================
# Enable Holiday
# =================================================

def enable_holiday(
    holiday_date: str,
) -> None:

    execute(
        """
        UPDATE holidays

        SET enabled=TRUE

        WHERE holiday_date=%s
        """,
        (
            holiday_date,
        ),
    )



# =================================================
# Disable Holiday
# =================================================

def disable_holiday(
    holiday_date: str,
) -> None:

    execute(
        """
        UPDATE holidays

        SET enabled=FALSE

        WHERE holiday_date=%s
        """,
        (
            holiday_date,
        ),
    )



# =================================================
# Is Holiday
# =================================================

def is_holiday(
    holiday_date: str,
) -> bool:

    row = fetch_one(
        """
        SELECT holiday_date

        FROM holidays

        WHERE holiday_date=%s

        AND enabled=TRUE

        LIMIT 1
        """,
        (
            holiday_date,
        ),
    )

    return row is not None



# =================================================
# All Holidays
# =================================================

def get_all_holidays() -> list[dict]:

    rows = fetch_all(
        """
        SELECT *

        FROM holidays

        ORDER BY holiday_date
        """
    )

    return [
        dict(row)
        for row in rows
    ]



# =================================================
# Active Holidays
# =================================================

def get_active_holidays() -> list[dict]:

    rows = fetch_all(
        """
        SELECT *

        FROM holidays

        WHERE enabled=TRUE

        ORDER BY holiday_date
        """
    )

    return [
        dict(row)
        for row in rows
    ]



# =================================================
# Admin Alias
# =================================================

def get_holidays() -> list[dict]:

    return get_all_holidays()
