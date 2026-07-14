"""
database/experts.py

Expert repository.
"""

from typing import Optional

from .crud import (
    execute,
    fetch_one,
    fetch_all,
)


# -------------------------------------------------
# Create / Update Expert
# -------------------------------------------------
def create_expert(
    chat_id: int,
    name: str,
    username: str = "",
    department: str = "",
) -> None:

    execute(
        """
        INSERT INTO experts
        (
            chat_id,
            name,
            username,
            department,
            is_active
        )

        VALUES
        (
            %s,
            %s,
            %s,
            %s,
            TRUE
        )

        ON CONFLICT(chat_id)

        DO UPDATE SET

            name = EXCLUDED.name,

            username = EXCLUDED.username,

            department = EXCLUDED.department
        """,
        (
            chat_id,
            name,
            username,
            department,
        ),
    )


# -------------------------------------------------
# Get Expert
# -------------------------------------------------
def get_expert(
    chat_id: int,
) -> Optional[dict]:

    row = fetch_one(
        """
        SELECT *

        FROM experts

        WHERE chat_id = %s
        """,
        (
            chat_id,
        ),
    )

    return dict(row) if row else None


# -------------------------------------------------
# List Experts
# -------------------------------------------------
def list_experts() -> list[dict]:

    rows = fetch_all(
        """
        SELECT *

        FROM experts

        ORDER BY

        is_active DESC,

        name
        """
    )

    return [
        dict(row)
        for row in rows
    ]


# -------------------------------------------------
# List Active Experts
# -------------------------------------------------
def list_active_experts() -> list[dict]:

    rows = fetch_all(
        """
        SELECT *

        FROM experts

        WHERE is_active = TRUE

        ORDER BY name
        """
    )

    return [
        dict(row)
        for row in rows
    ]


# -------------------------------------------------
# Update Department
# -------------------------------------------------
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


# -------------------------------------------------
# Activate / Deactivate
# -------------------------------------------------
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


def activate_expert(
    chat_id: int,
) -> None:

    set_active(
        chat_id,
        True,
    )


def deactivate_expert(
    chat_id: int,
) -> None:

    set_active(
        chat_id,
        False,
    )


# -------------------------------------------------
# Delete Expert
# -------------------------------------------------
def delete_expert(
    chat_id: int,
) -> None:

    execute(
        """
        DELETE FROM experts

        WHERE chat_id = %s
        """,
        (
            chat_id,
        ),
    )


# -------------------------------------------------
# Count Experts
# -------------------------------------------------
def count_experts() -> dict:

    row = fetch_one(
        """
        SELECT

        COUNT(*) AS total,

        COUNT(*) FILTER(
            WHERE is_active = TRUE
        ) AS active,

        COUNT(*) FILTER(
            WHERE is_active = FALSE
        ) AS inactive

        FROM experts
        """
    )

    return dict(row)


# -------------------------------------------------
# Exists
# -------------------------------------------------
def expert_exists(
    chat_id: int,
) -> bool:

    return get_expert(chat_id) is not None
