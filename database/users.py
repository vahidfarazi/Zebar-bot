"""
database/users.py

User repository.
"""

from typing import Optional

from .crud import execute, fetch_one, fetch_all


# -----------------------------
# Create User
# -----------------------------
def create_user(
    chat_id: int,
    username: str = "",
    full_name: str = "",
    role: str = "USER",
) -> None:
    """
    Create user if not exists.
    """

    execute(
        """
        INSERT INTO users
        (
            chat_id,
            username,
            full_name,
            role
        )
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (chat_id) DO NOTHING
        """,
        (
            chat_id,
            username,
            full_name,
            role,
        ),
    )


# -----------------------------
# Get User
# -----------------------------
def get_user(
    chat_id: int,
) -> Optional[dict]:

    row = fetch_one(
        """
        SELECT *
        FROM users
        WHERE chat_id = %s
        """,
        (chat_id,),
    )

    return dict(row) if row else None


# -----------------------------
# Update Username
# -----------------------------
def update_username(
    chat_id: int,
    username: str,
) -> None:

    execute(
        """
        UPDATE users
        SET username = %s
        WHERE chat_id = %s
        """,
        (
            username,
            chat_id,
        ),
    )


# -----------------------------
# Update Full Name
# -----------------------------
def update_full_name(
    chat_id: int,
    full_name: str,
) -> None:

    execute(
        """
        UPDATE users
        SET full_name = %s
        WHERE chat_id = %s
        """,
        (
            full_name,
            chat_id,
        ),
    )


# -----------------------------
# Update Role
# -----------------------------
def update_role(
    chat_id: int,
    role: str,
) -> None:

    execute(
        """
        UPDATE users
        SET role = %s
        WHERE chat_id = %s
        """,
        (
            role,
            chat_id,
        ),
    )


# -----------------------------
# Get All Users
# -----------------------------
def get_all_users() -> list[dict]:

    rows = fetch_all(
        """
        SELECT *
        FROM users
        ORDER BY created_at DESC
        """
    )

    return [dict(row) for row in rows]
