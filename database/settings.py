"""
database/settings.py

Settings repository.
"""

from typing import Optional

from .crud import execute, fetch_one


# -----------------------------
# Get Setting
# -----------------------------
def get_setting(key: str) -> Optional[str]:
    """
    Return setting value.
    """

    row = fetch_one(
        """
        SELECT value
        FROM settings
        WHERE key = %s
        """,
        (key,),
    )

    if row is None:
        return None

    return row["value"]


# -----------------------------
# Set Setting
# -----------------------------
def set_setting(
    key: str,
    value: str,
) -> None:
    """
    Create or update a setting.
    """

    execute(
        """
        INSERT INTO settings
        (
            key,
            value
        )
        VALUES (%s, %s)
        ON CONFLICT (key)
        DO UPDATE SET
            value = EXCLUDED.value
        """,
        (
            key,
            value,
        ),
    )
