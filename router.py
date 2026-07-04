"""
router.py

Central message router for Azarakhsh system.
"""

from handlers.user_handlers import handle_user_message
from handlers.admin_handlers import handle_admin_message
from handlers.expert_handlers import handle_expert_message
from handlers.tracking_handlers import handle_tracking_message


# -----------------------------
# Main Router
# -----------------------------
def route_message(chat_id: int, message: str, role: str = "USER") -> str:
    """
    Route incoming message to appropriate handler.
    """

    if not isinstance(message, str):
        message = ""

    message = message.strip()

    # Admin flow
    if role == "ADMIN":
        return handle_admin_message(chat_id, message)

    # Expert flow
    if role == "EXPERT":
        return handle_expert_message(chat_id, message)

    # Tracking has priority (keyword-based detection inside handler)
    tracking_response = handle_tracking_message(chat_id, message)
    if tracking_response:
        return tracking_response

    # Default user flow
    return handle_user_message(chat_id, message)
