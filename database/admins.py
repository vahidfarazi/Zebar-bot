"""
database/admins.py

Admin repository.
"""

from .crud import (
    execute,
    fetch_one,
    fetch_all,
)


# =================================================
# Add Admin
# =================================================

def add_admin(
    chat_id: int,
) -> None:
    """
    Add admin if not exists.
    """

    execute(
        """
        INSERT INTO admins
        (
            chat_id
        )

        VALUES
        (
            %s
        )

        ON CONFLICT(chat_id)

        DO NOTHING
        """,
        (
            chat_id,
        ),
    )


# =================================================
# Remove Admin
# =================================================

def remove_admin(
    chat_id: int,
) -> None:
    """
    Remove admin.
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


# =================================================
# Get Admin
# =================================================

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



# =================================================
# Is Admin
# =================================================

def is_admin(
    chat_id: int,
) -> bool:
    """
    Check admin.
    """

    return get_admin(
        chat_id
    ) is not None



# =================================================
# Active Compatibility
# =================================================

def set_active(
    chat_id: int,
    active: bool = True,
) -> None:
    """
    Compatibility function.

    Current schema has no active column,
    so this only keeps API compatibility.
    """

    if active:

        add_admin(
            chat_id
        )

    else:

        remove_admin(
            chat_id
        )



def activate_admin(
    chat_id: int,
) -> None:

    add_admin(
        chat_id
    )



def deactivate_admin(
    chat_id: int,
) -> None:

    remove_admin(
        chat_id
    )



# =================================================
# Active Admins
# =================================================

def get_active_admins() -> list[int]:
    """
    Current schema treats all admins as active.
    """

    return get_all_admins()



# =================================================
# All Admins
# =================================================

def get_all_admins() -> list[int]:

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



# =================================================
# Count
# =================================================

def count_admins() -> int:

    row = fetch_one(
        """
        SELECT COUNT(*) AS total

        FROM admins
        """
    )

    return int(
        row["total"] or 0
    )



# =================================================
# Exists
# =================================================

def admin_exists(
    chat_id: int,
) -> bool:

    return is_admin(
        chat_id
    )



# =================================================
# Dashboard
# =================================================

def get_dashboard_summary() -> dict:

    return {

        "admins":
            count_admins(),

        "active_admins":
            len(
                get_active_admins()
            ),

    }
