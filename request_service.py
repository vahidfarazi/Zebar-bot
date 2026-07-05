"""
request_service.py

Core business logic for request management.
"""

from typing import Dict, Any

from database import (
    insert_request,
    get_request_by_tracking,
    update_request_status,
)

from tracking_service import generate_tracking_code

from logger import (
    log_info,
    log_error,
)


# -----------------------------
# Create Request
# -----------------------------
def create_request(
    chat_id: int,
    title: str,
    description: str,
) -> Dict[str, Any]:
    """
    Create a new support request.
    """

    try:

        tracking_code = generate_tracking_code()

        request_id = insert_request(
            tracking_code,
            chat_id,
            title,
            description,
        )

        return {
            "success": True,
            "request_id": request_id,
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
            "message": "خطا در ثبت درخواست",
        }


# -----------------------------
# Get Request
# -----------------------------
def get_request_info(
    tracking_code: str,
) -> Dict[str, Any]:
    """
    Return request information.
    """

    try:

        request = get_request_by_tracking(
            tracking_code,
        )

        if request is None:

            return {
                "success": False,
                "message": "درخواستی یافت نشد.",
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


# -----------------------------
# Close Request
# -----------------------------
def close_request(
    request_id: int,
    user_id: int,
) -> Dict[str, Any]:
    """
    Close request.
    """

    try:

        update_request_status(
            request_id,
            "CLOSED",
        )

        log_info(
            "request_service",
            "close_request",
            f"{request_id} by {user_id}",
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
            "message": "خطا در بستن درخواست",
        }


# -----------------------------
# Reply (MVP)
# -----------------------------
def reply_request(
    request_id: int,
    sender_type: str,
    message: str,
) -> Dict[str, Any]:
    """
    Reply to request.
    """

    try:

        log_info(
            "request_service",
            "reply",
            f"{request_id} | {sender_type}",
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
            "message": "خطا در ثبت پاسخ",
        }
