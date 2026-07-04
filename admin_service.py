"""
admin_service.py

Business logic for admin operations:
- expert management
- system settings
- request transfer
- holiday management
- system control actions

NO SQL outside database.py
NO UI logic
"""

from datetime import datetime
from typing import Optional, List, Dict, Any

from database import execute, fetch_one, fetch_all
from logger import log_info, log_error, log_warning


# -----------------------------
# Create Expert
# -----------------------------
def create_expert(
    chat_id: int,
    name: str,
    username: str,
    department: str,
) -> bool:
    """
    Add new expert to system.
    """

    try:
        execute(
            """
            INSERT INTO experts (
                chat_id, name, username, department, active
            ) VALUES (?, ?, ?, ?, ?)
            """,
            (chat_id, name, username, department, 1),
        )

        log_info(
            "admin_service",
            "create_expert",
            f"expert={chat_id}",
            user_id=chat_id,
        )

        return True

    except Exception as e:
        log_error("admin_service", "create_expert_failed", str(e))
        return False


# -----------------------------
# Deactivate Expert
# -----------------------------
def remove_expert(chat_id: int) -> bool:
    """
    Soft delete expert (set inactive).
    """

    try:
        execute(
            """
            UPDATE experts
            SET active = 0
            WHERE chat_id = ?
            """,
            (chat_id,),
        )

        log_warning(
            "admin_service",
            "deactivate_expert",
            f"expert={chat_id}",
            user_id=chat_id,
        )

        return True

    except Exception as e:
        log_error("admin_service", "remove_expert_failed", str(e))
        return False


# -----------------------------
# Change System Settings (placeholder)
# -----------------------------
def change_settings(key: str, value: str) -> bool:
    """
    Update system settings in DB.
    """

    try:
        execute(
            """
            UPDATE settings
            SET value = ?
            WHERE key = ?
            """,
            (value, key),
        )

        log_info(
            "admin_service",
            "change_settings",
            f"{key}={value}",
        )

        return True

    except Exception as e:
        log_error("admin_service", "change_settings_failed", str(e))
        return False


# -----------------------------
# Holiday Management
# -----------------------------
def add_holiday(date: str) -> bool:
    """
    Add holiday date.
    """

    try:
        execute(
            """
            INSERT INTO holidays (holiday_date, enabled)
            VALUES (?, 1)
            """,
            (date,),
        )

        log_info(
            "admin_service",
            "add_holiday",
            f"date={date}",
        )

        return True

    except Exception as e:
        log_error("admin_service", "add_holiday_failed", str(e))
        return False


def remove_holiday(date: str) -> bool:
    """
    Disable holiday.
    """

    try:
        execute(
            """
            UPDATE holidays
            SET enabled = 0
            WHERE holiday_date = ?
            """,
            (date,),
        )

        log_warning(
            "admin_service",
            "remove_holiday",
            f"date={date}",
        )

        return True

    except Exception as e:
        log_error("admin_service", "remove_holiday_failed", str(e))
        return False


# -----------------------------
# Transfer Request
# -----------------------------
def transfer_request(tracking_code: str, new_expert_id: int) -> bool:
    """
    Transfer request to another expert.
    """

    try:
        request = fetch_one(
            "SELECT * FROM requests WHERE tracking_code = ?",
            (tracking_code,),
        )

        if not request:
            return False

        execute(
            """
            UPDATE requests
            SET expert_id = ?, status = ?, updated_at = ?
            WHERE tracking_code = ?
            """,
            (
                new_expert_id,
                "ASSIGNED",
                datetime.now().isoformat(),
                tracking_code,
            ),
        )

        log_info(
            "admin_service",
            "transfer_request",
            f"tracking={tracking_code}, new_expert={new_expert_id}",
        )

        return True

    except Exception as e:
        log_error("admin_service", "transfer_failed", str(e))
        return False


# -----------------------------
# Get Experts
# -----------------------------
def get_all_experts() -> List[Dict[str, Any]]:
    """
    Return all experts.
    """

    try:
        return fetch_all("SELECT * FROM experts")

    except Exception as e:
        log_error("admin_service", "get_all_experts_failed", str(e))
        return []
