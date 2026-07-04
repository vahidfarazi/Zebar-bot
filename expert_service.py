"""
expert_service.py

Business logic for expert operations.
Handles request assignment, replies, and closing by experts.
"""

from datetime import datetime

from database import (
    get_request_by_tracking,
    add_message_db,
    update_request_status,
    assign_request_to_expert,
)

from logger import log_info, log_warning


# -----------------------------
# Assign Request to Expert
# -----------------------------
def assign_request(request_id: int, expert_id: int) -> dict:
    """
    Assign request to an expert.
    """

    request = get_request_by_tracking(request_id)

    if not request:
        return {
            "success": False,
            "message": "REQUEST_NOT_FOUND",
        }

    assign_request_to_expert(request_id, expert_id)

    update_request_status(request_id, "ASSIGNED")

    log_info(
        "expert_service",
        "assign_request",
        f"request_id={request_id}, expert_id={expert_id}",
    )

    return {"success": True}


# -----------------------------
# Expert Reply
# -----------------------------
def reply(request_id: int, expert_id: int, message: str) -> dict:
    """
    Expert replies to a request.
    """

    request = get_request_by_tracking(request_id)

    if not request:
        return {
            "success": False,
            "message": "REQUEST_NOT_FOUND",
        }

    add_message_db(
        request_id=request_id,
        sender_type="EXPERT",
        message=message,
        created_at=datetime.now().isoformat(),
    )

    update_request_status(request_id, "WAITING_USER")

    log_info(
        "expert_service",
        "reply",
        f"request_id={request_id}, expert_id={expert_id}",
    )

    return {"success": True}


# -----------------------------
# Close Request by Expert
# -----------------------------
def close(request_id: int, expert_id: int) -> dict:
    """
    Close request by expert.
    """

    request = get_request_by_tracking(request_id)

    if not request:
        return {
            "success": False,
            "message": "REQUEST_NOT_FOUND",
        }

    update_request_status(request_id, "CLOSED")

    log_info(
        "expert_service",
        "close_request",
        f"request_id={request_id}, expert_id={expert_id}",
    )

    return {"success": True}


# -----------------------------
# Expert Warning Helper (future SLA logic)
# -----------------------------
def warn_if_unassigned(request_id: int) -> None:
    """
    Placeholder for SLA monitoring.
    """

    request = get_request_by_tracking(request_id)

    if not request:
        log_warning("expert_service", "sla_check_failed", f"id={request_id}")
        return

    if request.get("status") == "NEW":
        log_warning("expert_service", "unassigned_request", f"id={request_id}")
