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


# =================================================
# Create / Update Expert
# =================================================

def create_expert(
    chat_id: int,
    name: str,
    username: str = "",
    department: str = "",
    phone: str = "",
) -> None:
    """
    Create or update expert.
    """

    execute(
        """
        INSERT INTO experts
        (
            chat_id,
            name,
            username,
            department,
            phone,
            is_active
        )

        VALUES
        (
            %s,
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

            department = EXCLUDED.department,

            phone = EXCLUDED.phone
        """,
        (
            chat_id,
            name,
            username,
            department,
            phone,
        ),
    )


# =================================================
# Get Expert
# =================================================

def get_expert(
    chat_id: int,
) -> Optional[dict]:
    """
    Return expert by chat id.
    """

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



# =================================================
# Exists
# =================================================

def expert_exists(
    chat_id: int,
) -> bool:
    """
    Check expert existence.
    """

    return get_expert(chat_id) is not None



# =================================================
# List Experts
# =================================================

def list_experts() -> list[dict]:
    """
    Return all experts.
    """

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



# =================================================
# Active Experts
# =================================================

def list_active_experts() -> list[dict]:
    """
    Return active experts.
    """

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



# Compatibility aliases

def get_active_experts() -> list[dict]:
    return list_active_experts()



def get_active_expert(
    chat_id: int,
) -> Optional[dict]:

    return get_expert(
        chat_id,
    )



# =================================================
# Update Department
# =================================================

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



# =================================================
# Update Phone
# =================================================

def update_phone(
    chat_id: int,
    phone: str,
) -> None:

    execute(
        """
        UPDATE experts

        SET phone = %s

        WHERE chat_id = %s
        """,
        (
            phone,
            chat_id,
        ),
    )



# =================================================
# Activate / Deactivate
# =================================================

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



# =================================================
# Delete
# =================================================

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



# =================================================
# Count
# =================================================

def count_experts() -> dict:
    """
    Return expert counters.
    """

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

    if not row:
        return {
            "total": 0,
            "active": 0,
            "inactive": 0,
        }

    return {
        "total": row["total"] or 0,
        "active": row["active"] or 0,
        "inactive": row["inactive"] or 0,
    }
