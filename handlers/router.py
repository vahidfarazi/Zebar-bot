"""
router.py

Main entry point for all incoming messages.
Routes requests to appropriate handler modules.
"""

from handlers.user_handlers import handle_user_message
from handlers.admin_handlers import handle_admin_message
from handlers.expert_handlers import handle_expert_message
from handlers.tracking_handlers import handle_tracking_message


# -----------------------------
# Simple Role Router (MVP version)
# -----------------------------
def route_message(chat_id: int, message: str, role: str = "USER") -> str:
    """
    Route message based on user role.
    """

    if role == "ADMIN":
        return handle_admin_message(chat_id, message)

    if role == "EXPERT":
        return handle_expert_message(chat_id, message)

    # tracking has priority
    tracking_response = handle_tracking_message(chat_id, message)
    if tracking_response is not None:
        return tracking_response

    return handle_user_message(chat_id, message)
