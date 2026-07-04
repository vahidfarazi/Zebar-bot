"""
admin_handlers.py

Handles all ADMIN and SUPER_ADMIN operations:
- expert management
- request transfer
- system settings
- holidays
"""

from admin_service import (
    create_expert,
    deactivate_expert,
    transfer_request,
    add_holiday,
    remove_holiday,
    update_settings,
)

from database import get_request_by_tracking
from logger import log_info
from messages import GENERAL_ERROR, REQUEST_NOT_FOUND


# -----------------------------
# Handle Admin Message
# -----------------------------
def handle_admin_message(chat_id: int, message: str) -> str:
    """
    Process admin commands.
    """

    try:
        message = message.strip()

        # -------------------------
        # Add Expert
        # /add_expert chat_id|name|username|department
        # -------------------------
        if message.startswith("/add_expert"):
            parts = message.replace("/add_expert", "").strip().split("|")

            if len(parts) < 4:
                return "فرمت اشتباه است."

            chat_id_expert = int(parts[0].strip())
            name = parts[1].strip()
            username = parts[2].strip()
            department = parts[3].strip()

            result = create_expert(chat_id_expert, name, username, department)

            if result["success"]:
                log_info("admin_handlers", "add_expert", f"{chat_id_expert}")
                return "کارشناس با موفقیت اضافه شد."

            return result.get("message", GENERAL_ERROR)

        # -------------------------
        # Deactivate Expert
        # /remove_expert chat_id
        # -------------------------
        if message.startswith("/remove_expert"):
            expert_chat_id = int(message.replace("/remove_expert", "").strip())

            result = deactivate_expert(expert_chat_id)

            if result["success"]:
                log_info("admin_handlers", "remove_expert", f"{expert_chat_id}")
                return "کارشناس غیرفعال شد."

            return GENERAL_ERROR

        # -------------------------
        # Transfer Request
        # /transfer SR-2026-0000001|expert_id
        # -------------------------
        if message.startswith("/transfer"):
            parts = message.replace("/transfer", "").strip().split("|")

            if len(parts) < 2:
                return "فرمت اشتباه است."

            tracking = parts[0].strip()
            expert_id = int(parts[1].strip())

            request = get_request_by_tracking(tracking)

            if not request:
                return REQUEST_NOT_FOUND

            result = transfer_request(request["id"], expert_id)

            if result["success"]:
                log_info("admin_handlers", "transfer", f"{tracking} -> {expert_id}")
                return "درخواست منتقل شد."

            return GENERAL_ERROR

        # -------------------------
        # Add Holiday
        # /add_holiday YYYY-MM-DD
        # -------------------------
        if message.startswith("/add_holiday"):
            date = message.replace("/add_holiday", "").strip()

            result = add_holiday(date)

            if result["success"]:
                log_info("admin_handlers", "holiday_add", date)
                return "تعطیلی ثبت شد."

            return GENERAL_ERROR

        # -------------------------
        # Remove Holiday
        # /remove_holiday YYYY-MM-DD
        # -------------------------
        if message.startswith("/remove_holiday"):
            date = message.replace("/remove_holiday", "").strip()

            result = remove_holiday(date)

            if result["success"]:
                log_info("admin_handlers", "holiday_remove", date)
                return "تعطیلی حذف شد."

            return GENERAL_ERROR

        # -------------------------
        # Update Settings
        # /set key|value
        # -------------------------
        if message.startswith("/set"):
            parts = message.replace("/set", "").strip().split("|")

            if len(parts) < 2:
                return "فرمت اشتباه است."

            key = parts[0].strip()
            value = parts[1].strip()

            result = update_settings(key, value)

            if result["success"]:
                log_info("admin_handlers", "set", f"{key}={value}")
                return "تنظیمات بروزرسانی شد."

            return result.get("message", GENERAL_ERROR)

        # -------------------------
        # Default fallback
        # -------------------------
        return "دستور نامعتبر است."

    except Exception as e:
        log_info("admin_handlers", "error", str(e))
        return GENERAL_ERROR
