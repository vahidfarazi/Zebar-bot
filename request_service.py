"""
request_service.py

Core business logic for request management.
Handles creation, replies, closing and request lookup.
"""

from typing import Dict, Any

from database import (
    insert_request,
    get_request_by_tracking,
    update_request_status,
)

from services.tracking_service import generate_tracking_code

from logger import (
    log_info,
    log_error,
)


# -----------------------------
# Create Request
# -----------------------------
def create_request(chat_id: int, title: str, description: str) -> Dict[str, Any]:
    """
    Create a new support request.
    """

    try:
        tracking_code = generate_tracking_code()

        success = insert_request(
            tracking_code=tracking_code,
            chat_id=chat_id,
            title=title,
            description=description,
        )

        if not success:
            return {
                "success": False,
                "message": "خطا در ثبت درخواست"
            }

        log_info(
            "request_service",
            "create_request",
            f"{chat_id} -> {tracking_code}"
        )

        return {
            "success": True,
            "tracking_code": tracking_code,
        }

    except Exception as e:
        log_error(
            "request_service",
            "create_request",
            str(e),
        )

        return {
            "success": False,
            "message": "خطای داخلی سیستم",
        }


# -----------------------------
# Reply
# -----------------------------
def reply_request(
    request_id: int,
    sender_type: str,
    message: str,
) -> Dict[str, Any]:
    """
    Reply to request.
    MVP: only logging.
    """

    try:
        log_info(
            "request_service",
            "reply_request",
            f"request={request_id}, sender={sender_type}, message={message}",
        )

        return {
            "success": True,
        }

    except Exception as e:
        log_error(
            "request_service",
            "reply_request",
            str(e),
        )

        return {
            "success": False,
            "message": "خطا در ثبت پیام",
        }


# -----------------------------
# Close Request
# -----------------------------
def close_request(
    request_id: int,
    user_id: int,
) -> Dict[str, Any]:
    """
    Close support request.
    """

    try:
        success = update_request_status(
            request_id,
            "CLOSED",
        )

        if not success:
            return {
                "success": False,
                "message": "خطا در بستن درخواست",
            }

        log_info(
            "request_service",
            "close_request",
            f"request={request_id}, user={user_id}",
        )

        return {
            "success": True,
        }

    except Exception as e:
        log_error(
            "request_service",
            "close_request",
            str(e),
        )

        return {
            "success": False,
            "message": "خطای داخلی سیستم",
        }


# -----------------------------
# Get Request
# -----------------------------
def get_request_info(
    tracking_code: str,
) -> Dict[str, Any]:
    """
    Get request by tracking code.
    """

    try:
        request = get_request_by_tracking(
            tracking_code
        )

        if request is None:
            return {
                "success": False,
                "message": "درخواستی یافت نشد",
            }

        return {
            "success": True,
            "data": request,
        }

    except Exception as e:
        log_error(
            "request_service",
            "get_request_info",
            str(e),
        )

        return {
            "success": False,
            "message": "خطای داخلی سیستم",
        }
