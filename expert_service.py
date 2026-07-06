"""
expert_service.py

Business logic for expert operations (v1).
"""

from typing import Dict, Any

from database import (
    update_request_status,
    assign_expert,
    get_request_by_tracking,
    add_message,
)

from logger import (
    log_info,
    log_error,
)


# -----------------------------
# Reply
# -----------------------------
def reply(
    tracking_code: str,
    expert_id: int,
    message: str,
) -> Dict[str, Any]:
    """
    Expert reply to request.
    """

    try:

        request = get_request_by_tracking(tracking_code)

        if not request:
            return {
                "success": False,
                "message": "درخواست پیدا نشد",
            }

        # save expert message
        add_message(
            tracking_code=tracking_code,
            sender_type="EXPERT",
            sender_id=expert_id,
            message_type="REPLY",
            message=message,
        )

        log_info(
            "expert_service",
            "reply",
            f"{tracking_code} | {expert_id}",
        )

        return {
            "success": True,
        }

    except Exception as e:

        log_error(
            "expert_service",
            "reply",
            str(e),
        )

        return {
            "success": False,
            "message": "خطا در ثبت پاسخ",
        }


# -----------------------------
# Close Request
# -----------------------------
def close(
    tracking_code: str,
    expert_id: int,
) -> Dict[str, Any]:
    """
    Close request by expert.
    """

    try:

        request = get_request_by_tracking(tracking_code)

        if not request:
            return {
                "success": False,
                "message": "درخواست پیدا نشد",
            }

        update_request_status(
            request["id"],
            "CLOSED",
        )

        log_info(
            "expert_service",
            "close",
            f"{tracking_code} | {expert_id}",
        )

        return {
            "success": True,
        }

    except Exception as e:

        log_error(
            "expert_service",
            "close",
            str(e),
        )

        return {
            "success": False,
            "message": "خطای داخلی سیستم",
        }


# -----------------------------
# Assign Request
# -----------------------------
def assign_request(
    tracking_code: str,
    expert_id: int,
) -> Dict[str, Any]:
    """
    Assign request to expert.
    """

    try:

        request = get_request_by_tracking(tracking_code)

        if not request:
            return {
                "success": False,
                "message": "درخواست پیدا نشد",
            }

        assign_expert(
            request["id"],
            expert_id,
        )

        log_info(
            "expert_service",
            "assign",
            f"{tracking_code} -> {expert_id}",
        )

        return {
            "success": True,
        }

    except Exception as e:

        log_error(
            "expert_service",
            "assign",
            str(e),
        )

        return {
            "success": False,
            "message": "خطا در تخصیص درخواست",
        }
