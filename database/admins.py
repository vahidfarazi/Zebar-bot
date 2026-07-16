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

        WHERE chat_id=%s
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

        WHERE chat_id=%s

        LIMIT 1
        """,
        (
            chat_id,
        ),
    )

    if not row:
        return None

    return dict(row)



# =================================================
# Is Admin
# =================================================

def is_admin(
    chat_id: int,
) -> bool:
    """
    Check admin existence.
    """

    return get_admin(chat_id) is not None



# =================================================
# Activate / Deactivate
# =================================================

def activate_admin(
    chat_id: int,
) -> None:
    """
    Activate admin.
    """

    add_admin(chat_id)



def deactivate_admin(
    chat_id: int,
) -> None:
    """
    Deactivate admin.

    Current schema removes admin.
    """

    remove_admin(chat_id)



def set_active(
    chat_id: int,
    active: bool = True,
) -> None:
    """
    Compatibility wrapper.
    """

    if active:
        activate_admin(chat_id)

    else:
        deactivate_admin(chat_id)



# =================================================
# All Admins
# =================================================

def get_all_admins() -> list[int]:
    """
    Return all admins.
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



# =================================================
# Active Admins
# =================================================

def get_active_admins() -> list[int]:
    """
    Current schema:
    all existing admins are active.
    """

    return get_all_admins()



# =================================================
# Count
# =================================================

def count_admins() -> int:
    """
    Count admins.
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



# =================================================
# Exists
# =================================================

def admin_exists(
    chat_id: int,
) -> bool:
    """
    Check admin existence.
    """

    return is_admin(chat_id)



# =================================================
# Dashboard
# =================================================

def get_dashboard_summary() -> dict:
    """
    Admin dashboard summary.
    """

    return {

        "admins":
            count_admins(),

        "active_admins":
            len(
                get_active_admins()
            ),

    }
