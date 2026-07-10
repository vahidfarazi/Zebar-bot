"""
database/experts.py

Expert repository.
"""

from typing import Optional

from .crud import execute, fetch_one, fetch_all


# -----------------------------
# Create Expert
# -----------------------------
def create_expert(
    chat_id: int,
    name: str,
    username: str = "",
    department: str = "",
) -> None:
    """
    Create expert if not exists.
    """

    execute(
        """
        INSERT INTO experts
        (
            chat_id,
            name,
            username,
            department
        )
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (chat_id) DO NOTHING
        """,
        (
            chat_id,
            name,
            username,
            department,
        ),
    )


# -----------------------------
# Get Expert
# -----------------------------
def get_expert(
    chat_id: int,
) -> Optional[dict]:

    row = fetch_one(
        """
        SELECT *
        FROM experts
        WHERE chat_id = %s
        """,
        (chat_id,),
    )

    return dict(row) if row else None


# -----------------------------
# List Active Experts
# -----------------------------
def list_active_experts() -> list[dict]:

    rows = fetch_all(
        """
        SELECT *
        FROM experts
        WHERE is_active = TRUE
        ORDER BY name
        """
    )

    return [dict(row) for row in rows]


# -----------------------------
# Update Department
# -----------------------------
def update_department(
    chat_id: int,
    department: str,
) -> None:

    execute(
        """
        UPDATE experts
        SET department = %s
        WHERE chat_id = %s
        """,
        (
            department,
            chat_id,
        ),
    )


# -----------------------------
# Set Active
# -----------------------------
def set_active(
    chat_id: int,
    active: bool,
) -> None:

    execute(
        """
        UPDATE experts
        SET is_active = %s
        WHERE chat_id = %s
        """,
        (
            active,
            chat_id,
        ),
    )


# -----------------------------
# Delete Expert
# -----------------------------
def delete_expert(
    chat_id: int,
) -> None:

    execute(
        """
        DELETE FROM experts
        WHERE chat_id = %s
        """,
        (chat_id,),
    )
