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
        INSERT OR IGNORE INTO experts
        (
            chat_id,
            name,
            username,
            department
        )
        VALUES (?, ?, ?, ?)
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
        WHERE chat_id = ?
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
        WHERE is_active = 1
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
        SET department = ?
        WHERE chat_id = ?
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
        SET is_active = ?
        WHERE chat_id = ?
        """,
        (
            1 if active else 0,
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
        WHERE chat_id = ?
        """,
        (chat_id,),
    )
