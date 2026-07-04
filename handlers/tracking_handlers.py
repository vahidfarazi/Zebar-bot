"""
tracking_handlers.py

Handles tracking code queries for users, experts, and admins.
"""

from tracking import validate_tracking
from database import get_request_by_tracking
from logger import log_info
from messages import (
    INVALID_TRACKING,
    REQUEST_NOT_FOUND,
)


# -----------------------------
# Handle Tracking Message
# -----------------------------
def handle_tracking_message(chat_id: int, message: str):
    """
    If message is a tracking code, return request info.
    Otherwise return None (so router continues flow).
    """

    message = message.strip()

    # -------------------------
    # Check if message is tracking code
    # -------------------------
    if not validate_tracking(message):
        return None  # not tracking → pass to next handler

    log_info("tracking_handlers", "search", f"user={chat_id}, code={message}")

    request = get_request_by_tracking(message)

    # -------------------------
    # Not found
    # -------------------------
    if not request:
        return REQUEST_NOT_FOUND

    # -------------------------
    # Format response
    # -------------------------
    response = f"""
📌 Tracking: {request['tracking_code']}
📊 Status: {request['status']}
🧾 Title: {request.get('title', '-')}

📅 Created: {request.get('created_at', '-')}

🔄 Updated: {request.get('updated_at', '-')}
"""

    return response
