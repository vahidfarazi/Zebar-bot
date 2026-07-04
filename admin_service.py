"""
admin_service.py

Business logic for admin operations.
Handles experts, settings, holidays, and request management.
"""

from datetime import datetime

from database import (
    create_expert_db,
    update_expert_status,
    get_expert_by_chat_id,
    transfer_request_db,
    add_holiday_db,
    remove_holiday_db,
    update_settings_db,
    get_request_by_tracking,
    update_request_status,
    assign_request_to_expert,
)

from logger import log_info, log_warning


# -----------------------------
# Create Expert
# -----------------------------
def create_expert(chat_id: int, name: str, username: str, department: str) -> dict:
    """
    Add new expert to system.
    """

    existing = get_expert_by_chat_id(chat_id)

    if existing:
        return {
            "success": False,
            "message": "EXPERT_ALREADY_EXISTS",
        }

    expert_id = create_expert_db(
        chat_id=chat_id,
        name=name,
        username=username,
        department=department,
        active=1,
    )

    log_info("admin_service", "create_expert", f"chat_id={chat_id}")

    return {
        "success": True,
        "expert_id": expert_id,
    }


# -----------------------------
# Deactivate Expert
# -----------------------------
def deactivate_expert(chat_id: int) -> dict:
    """
    Deactivate an expert (soft delete).
    """

    expert = get_expert_by_chat_id(chat_id)

    if not expert:
        return {
            "success": False,
            "message": "EXPERT_NOT_FOUND",
        }

    update_expert_status(chat_id, 0)

    log_warning("admin_service", "deactivate_expert", f"chat_id={chat_id}")

    return {"success": True}


# -----------------------------
# Transfer Request
# -----------------------------
def transfer_request(request_id: int, new_expert_id: int) -> dict:
    """
    Transfer request to another expert.
    """

    request = get_request_by_tracking(request_id)

    if not request:
        return {
            "success": False,
            "message": "REQUEST_NOT_FOUND",
        }

    transfer_request_db(request_id, new_expert_id)

    update_request_status(request_id, "ASSIGNED")

    log_info(
        "admin_service",
        "transfer_request",
        f"request_id={request_id}, new_expert={new_expert_id}",
    )

    return {"success": True}


# -----------------------------
# Add Holiday
# -----------------------------
def add_holiday(date: str) -> dict:
    """
    Add holiday to system.
    """

    add_holiday_db(date)

    log_info("admin_service", "add_holiday", f"date={date}")

    return {"success": True}


# -----------------------------
# Remove Holiday
# -----------------------------
def remove_holiday(date: str) -> dict:
    """
    Remove holiday from system.
    """

    remove_holiday_db(date)

    log_warning("admin_service", "remove_holiday", f"date={date}")

    return {"success": True}


# -----------------------------
# Update System Settings
# -----------------------------
def update_settings(key: str, value: str) -> dict:
    """
    Update system configuration.
    """

    allowed_keys = [
        "WORK_START",
        "WORK_END",
        "SYSTEM_MODE",
        "ALLOW_NEW_REQUEST",
        "ALLOW_TRACKING",
        "MAX_UPLOAD_SIZE",
    ]

    if key not in allowed_keys:
        return {
            "success": False,
            "message": "INVALID_SETTING_KEY",
        }

    update_settings_db(key, value)

    log_info("admin_service", "update_settings", f"{key}={value}")

    return {"success": True}
