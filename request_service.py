"""
request_service.py

Core business logic for request management.
Handles creation, replies, closing, and SLA base flow.
"""

from typing import Dict, Any
from database import (
    insert_request,
    get_request_by_tracking,
    update_request_status,
)
from tracking import generate_tracking
from logger import log_info, log_error


# -----------------------------
# Create Request
# -----------------------------
def create_request(chat_id: int, title: str, description: str) -> Dict[str, Any]:
    """
    Create a new support request.
    """

    try:
        tracking_code = generate_tracking(chat_id)

        success = insert_request(tracking_code, chat_id, title, description)

        if not success:
            return {
                "success": False,
                "message": "خطا در ثبت درخواست"
            }

        log_info("request_service", "create_request", f"{chat_id} -> {tracking_code}")

        return {
            "success": True,
            "tracking_code": tracking_code
        }

    except Exception as e:
        log_error("request_service", "create_request", str(e))
        return {
            "success": False,
            "message": "خطای داخلی سیستم"
        }


# -----------------------------
# Reply to Request
# -----------------------------
def reply_request(request_id: int, sender_type: str, message: str) -> Dict[str, Any]:
    """
    Add reply to a request (MVP simplified).
    """

    try:
        # MVP: فقط لاگ می‌کنیم (در نسخه بعد جدول messages اضافه می‌شود)
        log_info(
            "request_service",
            "reply",
            f"request={request_id}, sender={sender_type}, msg={message}"
        )

        return {
            "success": True
        }

    except Exception as e:
        log_error("request_service", "reply_request", str(e))
        return {
            "success": False,
            "message": "خطا در ثبت پیام"
        }


# -----------------------------
# Close Request
# -----------------------------
def close_request(request_id: int, user_id: int) -> Dict[str, Any]:
    """
    Close a request.
    """

    try:
        success = update_request_status(request_id, "CLOSED")

        if not success:
            return {
                "success": False,
                "message": "خطا در بستن درخواست"
            }

        log_info("request_service", "close_request", f"{request_id} by {user_id}")

        return {
            "success": True
        }

    except Exception as e:
        log_error("request_service", "close_request", str(e))
        return {
            "success": False,
            "message": "خطای داخلی سیستم"
        }


# -----------------------------
# Get Request Info
# -----------------------------
def get_request_info(tracking_code: str) -> Dict[str, Any]:
    """
    Return full request info.
    """

    try:
        request = get_request_by_tracking(tracking_code)

        if not request:
            return {
                "success": False,
                "message": "درخواستی یافت نشد"
            }

        return {
            "success": True,
            "data": request
        }

    except Exception as e:
        log_error("request_service", "get_request_info", str(e))
        return {
            "success": False,
            "message": "خطای داخلی سیستم"
        }
