"""
database/admins.py

Admin repository.
"""

from .crud import execute, fetch_one, fetch_all


# -----------------------------
# Add Admin
# -----------------------------
def add_admin(chat_id: int) -> None:
    """
    Add new admin.
    """

    execute(
        """
        INSERT INTO admins
        (
            chat_id
        )
        VALUES (%s)
        ON CONFLICT (chat_id) DO NOTHING
        """,
        (chat_id,),
    )


# -----------------------------
# Remove Admin
# -----------------------------
def remove_admin(chat_id: int) -> None:
    """
    Remove admin.
    """

    execute(
        """
        DELETE FROM admins
        WHERE chat_id = %s
        """,
        (chat_id,),
    )


# -----------------------------
# Is Admin
# -----------------------------
def is_admin(chat_id: int) -> bool:
    """
    Check whether user is admin.
    """

    row = fetch_one(
        """
        SELECT chat_id
        FROM admins
        WHERE chat_id = %s
        """,
        (chat_id,),
    )

    return row is not None


# -----------------------------
# Get All Admins
# -----------------------------
def get_all_admins() -> list[int]:
    """
    Return all admin chat IDs.
    """

    rows = fetch_all(
        """
        SELECT chat_id
        FROM admins
        ORDER BY chat_id
        """
    )

    return [row["chat_id"] for row in rows]
