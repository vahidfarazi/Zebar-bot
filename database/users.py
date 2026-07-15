"""
database/users.py

User repository.
"""

from typing import Optional

from .crud import (
    execute,
    fetch_one,
    fetch_all,
)


# =================================================
# Create User
# =================================================

def create_user(
    chat_id: int,
    username: str = "",
    full_name: str = "",
    role: str = "USER",
) -> None:
    """
    Create or update user.
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

        VALUES
        (
            %s,
            %s,
            %s,
            %s
        )

        ON CONFLICT(chat_id)

        DO UPDATE SET

            username = EXCLUDED.username,

            full_name = EXCLUDED.full_name,

            role = EXCLUDED.role
        """,
        (
            chat_id,
            username,
            full_name,
            role,
        ),
    )


# =================================================
# Get User
# =================================================

def get_user(
    chat_id: int,
) -> Optional[dict]:
    """
    Return user by chat id.
    """

    row = fetch_one(
        """
        SELECT *

        FROM users

        WHERE chat_id = %s
        """,
        (
            chat_id,
        ),
    )

    return dict(row) if row else None



# Compatibility Alias

def get_user_by_chat_id(
    chat_id: int,
) -> Optional[dict]:

    return get_user(
        chat_id
    )



# =================================================
# Update Username
# =================================================

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



# =================================================
# Update Full Name
# =================================================

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



# =================================================
# Update Role
# =================================================

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



# =================================================
# Delete User
# =================================================

def delete_user(
    chat_id: int,
) -> None:

    execute(
        """
        DELETE FROM users

        WHERE chat_id = %s
        """,
        (
            chat_id,
        ),
    )



# =================================================
# Exists
# =================================================

def user_exists(
    chat_id: int,
) -> bool:

    return get_user(
        chat_id
    ) is not None



# =================================================
# All Users
# =================================================

def get_all_users() -> list[dict]:

    rows = fetch_all(
        """
        SELECT *

        FROM users

        ORDER BY created_at DESC
        """
    )

    return [
        dict(row)
        for row in rows
    ]



# Compatibility Alias

def get_users() -> list[dict]:

    return get_all_users()



# =================================================
# Count Users
# =================================================

def count_users() -> int:

    row = fetch_one(
        """
        SELECT COUNT(*) AS total

        FROM users
        """
    )

    if not row:
        return 0

    return int(
        row["total"] or 0
    )
