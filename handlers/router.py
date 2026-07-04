"""
router.py

Main entry point for routing messages based on role and stored state.
"""

from handlers.user_handlers import handle_user_message
from handlers.admin_handlers import handle_admin_message
from handlers.expert_handlers import handle_expert_message
from handlers.tracking_handlers import handle_tracking_message

from state_manager import get_user_state


# -----------------------------
# Main Router
# -----------------------------
def route_message(chat_id: int, message: str, role: str = "USER") -> str:
    """
    Route message based on role and stored conversation state.
    """

    # گرفتن state واقعی از دیتابیس
    state = get_user_state(chat_id)

    # -----------------------------
    # ADMIN
    # -----------------------------
    if role == "ADMIN":
        return handle_admin_message(chat_id, message, state)

    # -----------------------------
    # EXPERT
    # -----------------------------
    if role == "EXPERT":
        return handle_expert_message(chat_id, message, state)

    # -----------------------------
    # USER FLOW (STATE BASED)
    # -----------------------------

    if state == "TRACKING":
        return handle_tracking_message(chat_id, message)

    if state == "CHAT_WITH_EXPERT":
        return handle_expert_message(chat_id, message)

    if state == "CREATING_REQUEST":
        return handle_user_message(chat_id, message, state)

    return handle_user_message(chat_id, message, state)
