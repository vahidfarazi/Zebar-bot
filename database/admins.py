"""
database/admins.py

Admin repository.
"""

from .crud import (
    execute,
    fetch_one,
    fetch_all,
)


# -------------------------------------------------
# Add Admin
# -------------------------------------------------
def add_admin(
    chat_id: int,
    active: bool = True,
) -> None:
    """
    Add new admin or activate existing one.
    """

    execute(
        """
        INSERT INTO admins
        (
            chat_id,
            active
        )

        VALUES
        (
            %s,
            %s
        )

        ON CONFLICT(chat_id)

        DO UPDATE SET

            active = EXCLUDED.active
        """,
        (
            chat_id,
            active,
        ),
    )


# -------------------------------------------------
# Remove Admin
# -------------------------------------------------
def remove_admin(
    chat_id: int,
) -> None:
    """
    Remove admin completely.
    """

    execute(
        """
        DELETE FROM admins

        WHERE chat_id = %s
        """,
        (
            chat_id,
        ),
    )


# -------------------------------------------------
# Get Admin
# -------------------------------------------------
def get_admin(
    chat_id: int,
) -> dict | None:
    """
    Return admin record.
    """

    row = fetch_one(
        """
        SELECT *

        FROM admins

        WHERE chat_id = %s
        """,
        (
            chat_id,
        ),
    )

    return dict(row) if row else None


# -------------------------------------------------
# Is Admin
# -------------------------------------------------
def is_admin(
    chat_id: int,
) -> bool:
    """
    Check admin existence.
    """

    return get_admin(chat_id) is not None


# -------------------------------------------------
# Activate / Deactivate
# -------------------------------------------------
def set_active(
    chat_id: int,
    active: bool = True,
) -> None:
    """
    Enable / Disable admin.
    """

    execute(
        """
        UPDATE admins

        SET active = %s

        WHERE chat_id = %s
        """,
        (
            active,
            chat_id,
        ),
    )


def activate_admin(
    chat_id: int,
) -> None:

    set_active(
        chat_id,
        True,
    )


def deactivate_admin(
    chat_id: int,
) -> None:

    set_active(
        chat_id,
        False,
    )


# -------------------------------------------------
# Active Admins
# -------------------------------------------------
def get_active_admins() -> list[int]:
    """
    Return active admin ids.
    """

    rows = fetch_all(
        """
        SELECT chat_id

        FROM admins

        WHERE active = TRUE

        ORDER BY chat_id
        """
    )

    return [
        row["chat_id"]
        for row in rows
    ]


# -------------------------------------------------
# All Admins
# -------------------------------------------------
def get_all_admins() -> list[int]:
    """
    Return all admin ids.
    """

    rows = fetch_all(
        """
        SELECT chat_id

        FROM admins

        ORDER BY chat_id
        """
    )

    return [
        row["chat_id"]
        for row in rows
    ]


# -------------------------------------------------
# Count
# -------------------------------------------------
def count_admins() -> int:
    """
    Total admins.
    """

    row = fetch_one(
        """
        SELECT COUNT(*) AS total

        FROM admins
        """
    )

    return int(
        row["total"] or 0
    )


# -------------------------------------------------
# Exists
# -------------------------------------------------
def admin_exists(
    chat_id: int,
) -> bool:

    return is_admin(
        chat_id
    )


# -------------------------------------------------
# Dashboard
# -------------------------------------------------
def get_dashboard_summary() -> dict:
    """
    Admin statistics.
    """

    return {

        "admins":
            count_admins(),

        "active_admins":
            len(
                get_active_admins()
            ),

    }
