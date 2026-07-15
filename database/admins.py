"""
database/admins.py

Admin repository.
"""

from .crud import execute, fetch_one, fetch_all


# -------------------------------------------------
# Add Admin
# -------------------------------------------------
def add_admin(chat_id: int) -> None:
    execute(
        """
        INSERT INTO admins(chat_id)
        VALUES (%s)
        ON CONFLICT(chat_id)
        DO NOTHING
        """,
        (chat_id,),
    )


# -------------------------------------------------
# Remove Admin
# -------------------------------------------------
def remove_admin(chat_id: int) -> None:
    execute(
        """
        DELETE FROM admins
        WHERE chat_id=%s
        """,
        (chat_id,),
    )


# -------------------------------------------------
# Is Admin
# -------------------------------------------------
def is_admin(chat_id: int) -> bool:
    row = fetch_one(
        """
        SELECT chat_id
        FROM admins
        WHERE chat_id=%s
        """,
        (chat_id,),
    )

    return row is not None


# -------------------------------------------------
# Set Active Admin
# -------------------------------------------------
def set_active(chat_id: int, active: bool = True) -> None:

    execute(
        """
        UPDATE admins
        SET active=%s
        WHERE chat_id=%s
        """,
        (
            active,
            chat_id,
        ),
    )


# -------------------------------------------------
# Get Active Admins
# -------------------------------------------------
def get_active_admins() -> list[int]:

    rows = fetch_all(
        """
        SELECT chat_id
        FROM admins
        WHERE active=true
        ORDER BY chat_id
        """
    )

    return [
        row["chat_id"]
        for row in rows
    ]


# -------------------------------------------------
# Get All Admins
# -------------------------------------------------
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


# -------------------------------------------------
# Count Admins
# -------------------------------------------------
def count_admins() -> int:

    row = fetch_one(
        """
        SELECT COUNT(*) AS total
        FROM admins
        """
    )

    return int(row["total"])


# -------------------------------------------------
# Admin Exists
# -------------------------------------------------
def admin_exists(chat_id: int) -> bool:
    return is_admin(chat_id)


# -------------------------------------------------
# Dashboard helper
# -------------------------------------------------
def get_dashboard_summary():

    return {
        "admins": count_admins(),
        "active_admins": len(get_active_admins()),
    }
