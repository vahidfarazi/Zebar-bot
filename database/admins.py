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
# Is Admin
# =================================================

def is_admin(
    chat_id: int,
) -> bool:

    row = fetch_one(
        """
        SELECT chat_id

        FROM admins

        WHERE chat_id=%s

        LIMIT 1
        """,
        (
            chat_id,
        ),
    )

    return row is not None



# =================================================
# Get All Admins
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
# Count Admins
# =================================================

def count_admins() -> int:

    row = fetch_one(
        """
        SELECT COUNT(*) AS total

        FROM admins
        """
    )

    return int(row["total"] or 0)



# =================================================
# Admin Exists
# =================================================

def admin_exists(
    chat_id: int,
) -> bool:

    return is_admin(
        chat_id
    )



# =================================================
# Set Active
# Compatibility Function
# =================================================

def set_active(
    chat_id: int,
    active: bool,
) -> None:

    """
    Compatibility method.

    Current admins table does not have active column.
    Existing admins are considered active.
    """

    return None



# =================================================
# Get Active Admins
# Compatibility Function
# =================================================

def get_active() -> list[int]:

    return get_all_admins()



# =================================================
# Enable Admin
# =================================================

def enable_admin(
    chat_id: int,
) -> None:

    add_admin(
        chat_id
    )



# =================================================
# Disable Admin
# =================================================

def disable_admin(
    chat_id: int,
) -> None:

    remove_admin(
        chat_id
    )
