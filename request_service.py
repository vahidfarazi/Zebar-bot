"""
request_service.py

Core business logic for requests.
Handles request lifecycle: create, reply, close, priority.
"""

from datetime import datetime

from database import (
    create_request_db,
    get_request_by_tracking,
    add_message_db,
    update_request_status,
    update_request_priority,
)

from tracking import generate_tracking_code
from working_hours import can_create_request
from logger import log_info, log_warning


# -----------------------------
# Create Request
# -----------------------------
def create_request(user_id: int, title: str, description: str) -> dict:
    """
    Create a new service request.
    """

    if not can_create_request():
        log_warning("request_service", "create_blocked", f"user={user_id}")
        return {
            "success": False,
            "message": "OUT_OF_WORK_TIME",
        }

    tracking_code = generate_tracking_code()

    request_id = create_request_db(
        user_id=user_id,
        tracking_code=tracking_code,
        title=title,
        description=description,
        status="NEW",
        priority="NORMAL",
        created_at=datetime.now().isoformat(),
    )

    log_info("request_service", "create_request", f"tracking={tracking_code}")

    return {
        "success": True,
        "tracking_code": tracking_code,
        "request_id": request_id,
    }


# -----------------------------
# Reply to Request
# -----------------------------
def reply_request(request_id: int, sender_type: str, message: str) -> dict:
    """
    Add message to request conversation.
    """

    request = get_request_by_tracking(request_id)

    if not request:
        return {
            "success": False,
            "message": "REQUEST_NOT_FOUND",
        }

    add_message_db(
        request_id=request_id,
        sender_type=sender_type,
        message=message,
        created_at=datetime.now().isoformat(),
    )

    # status switch logic
    if sender_type == "USER":
        update_request_status(request_id, "WAITING_EXPERT")
    else:
        update_request_status(request_id, "WAITING_USER")

    log_info("request_service", "reply", f"request_id={request_id}")

    return {"success": True}


# -----------------------------
# Close Request
# -----------------------------
def close_request(request_id: int, closed_by: str) -> dict:
    """
    Close a request.
    """

    request = get_request_by_tracking(request_id)

    if not request:
        return {
            "success": False,
            "message": "REQUEST_NOT_FOUND",
        }

    update_request_status(request_id, "CLOSED")

    log_info("request_service", "close_request", f"id={request_id}, by={closed_by}")

    return {"success": True}


# -----------------------------
# Change Priority
# -----------------------------
def change_priority(request_id: int, priority: str) -> dict:
    """
    Update request priority.
    """

    valid_priorities = ["LOW", "NORMAL", "HIGH", "URGENT"]

    if priority not in valid_priorities:
        return {
            "success": False,
            "message": "INVALID_PRIORITY",
        }

    update_request_priority(request_id, priority)

    log_info("request_service", "change_priority", f"id={request_id}, p={priority}")

    return {"success": True}
