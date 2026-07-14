"""
database/settings.py

Settings repository.
"""

from typing import Optional

from .crud import (
    execute,
    fetch_one,
    fetch_all,
)


# -------------------------------------------------
# Get Setting
# -------------------------------------------------
def get_setting(
    key: str,
    default: Optional[str] = None,
) -> Optional[str]:
    """
    Return setting value.
    """

    row = fetch_one(

        """
        SELECT value

        FROM settings

        WHERE key = %s
        """,

        (
            key,
        ),

    )

    if not row:

        return default

    return row.get(
        "value",
        default,
    )


# -------------------------------------------------
# Set Setting
# -------------------------------------------------
def set_setting(
    key: str,
    value: str,
) -> None:
    """
    Create or update setting.
    """

    execute(

        """
        INSERT INTO settings
        (
            key,
            value
        )

        VALUES
        (
            %s,
            %s
        )

        ON CONFLICT (key)

        DO UPDATE SET

            value = EXCLUDED.value
        """,

        (
            key,
            value,
        ),

    )


# -------------------------------------------------
# Delete Setting
# -------------------------------------------------
def delete_setting(
    key: str,
) -> None:

    execute(

        """
        DELETE FROM settings

        WHERE key = %s
        """,

        (
            key,
        ),

    )


# -------------------------------------------------
# Get All Settings
# -------------------------------------------------
def get_all_settings() -> list[dict]:
    """
    Return all settings.
    """

    rows = fetch_all(

        """
        SELECT *

        FROM settings

        ORDER BY key
        """

    )

    return [

        dict(row)

        for row in rows

    ]


# -------------------------------------------------
# Working Hours
# -------------------------------------------------
def get_working_hours() -> dict:
    """
    Get working configuration.
    """

    return {

        "start":
            get_setting(
                "WORK_START",
                "07:00",
            ),

        "end":
            get_setting(
                "WORK_END",
                "13:00",
            ),

        "days":
            get_setting(
                "WORK_DAYS",
                "شنبه,یکشنبه,دوشنبه,سه‌شنبه,چهارشنبه",
            ),

    }


def set_working_hours(
    start: str,
    end: str,
    days: str,
) -> None:
    """
    Update working hours.
    """

    set_setting(
        "WORK_START",
        start,
    )

    set_setting(
        "WORK_END",
        end,
    )

    set_setting(
        "WORK_DAYS",
        days,
    )


# -------------------------------------------------
# Boolean Settings
# -------------------------------------------------
def get_bool_setting(
    key: str,
    default: bool = False,
) -> bool:
    """
    Read boolean settings safely.
    """

    value = get_setting(
        key,
    )

    if value is None:

        return default

    return value.lower() in (
        "1",
        "true",
        "yes",
        "on",
        "فعال",
    )


def set_bool_setting(
    key: str,
    value: bool,
) -> None:
    """
    Save boolean setting.
    """

    set_setting(

        key,

        "true"
        if value
        else "false",

    )
