"""
expert_service.py

Business logic for expert operations:
- reply to requests
- close requests
- expert actions handling
"""

from typing import Dict, Any
from database import update_request_status
from logger import log_info, log_error


# -----------------------------
# Reply to Request
# -----------------------------
def reply(request_id: int, expert_id: int, message: str) -> Dict[str, Any]:
    """
    Expert replies to a request.
    """

    try:
        # MVP: فقط لاگ می‌کنیم (در نسخه 1.1 جدول پیام‌ها اضافه می‌شود)
        log_info(
            "expert_service",
            "reply",
            f"request={request_id}, expert={expert_id}, msg={message}"
        )

        return {
            "success": True
        }

    except Exception as e:
        log_error("expert_service", "reply", str(e))
        return {
            "success": False,
            "message": "خطا در ثبت پاسخ"
        }


# -----------------------------
# Close Request
# -----------------------------
def close(request_id: int, expert_id: int) -> Dict[str, Any]:
    """
    Close request by expert.
    """

    try:
        success = update_request_status(request_id, "CLOSED")

        if not success:
            return {
                "success": False,
                "message": "خطا در بستن درخواست"
            }

        log_info(
            "expert_service",
            "close",
            f"request={request_id}, expert={expert_id}"
        )

        return {
            "success": True
        }

    except Exception as e:
        log_error("expert_service", "close", str(e))
        return {
            "success": False,
            "message": "خطای داخلی سیستم"
        }


# -----------------------------
# Assign Request (MVP placeholder)
# -----------------------------
def assign_request(request_id: int, expert_id: int) -> Dict[str, Any]:
    """
    Assign request to expert (simplified MVP version).
    """

    try:
        # MVP: فقط لاگ (در نسخه بعد column اختصاصی اضافه می‌شود)
        log_info(
            "expert_service",
            "assign",
            f"request={request_id} -> expert={expert_id}"
        )

        return {
            "success": True
        }

    except Exception as e:
        log_error("expert_service", "assign", str(e))
        return {
            "success": False,
            "message": "خطا در تخصیص درخواست"
        }
