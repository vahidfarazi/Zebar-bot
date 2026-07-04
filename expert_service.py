"""
expert_service.py

Business logic for expert operations.
"""

from typing import Dict, Any

from database import (
    update_request_status,
    assign_expert,
)

from logger import (
    log_info,
    log_error,
)


# -----------------------------
# Reply
# -----------------------------
def reply(
    request_id: int,
    expert_id: int,
    message: str,
) -> Dict[str, Any]:
    """
    Expert reply to request.
    """

    try:

        log_info(
            "expert_service",
            "reply",
            f"{request_id} | {expert_id}",
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
# Close
# -----------------------------
def close(
    request_id: int,
    expert_id: int,
) -> Dict[str, Any]:
    """
    Close request by expert.
    """

    try:

        update_request_status(
            request_id,
            "CLOSED",
        )

        log_info(
            "expert_service",
            "close",
            f"{request_id} | {expert_id}",
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
# Assign
# -----------------------------
def assign_request(
    request_id: int,
    expert_id: int,
) -> Dict[str, Any]:
    """
    Assign request to expert.
    """

    try:

        assign_expert(
            request_id,
            expert_id,
        )

        log_info(
            "expert_service",
            "assign",
            f"{request_id} -> {expert_id}",
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
