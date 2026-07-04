"""
router.py

Main entry point for all incoming messages.
Routes requests to appropriate handler modules based on role and state.
"""

from handlers.user_handlers import handle_user_message
from handlers.admin_handlers import handle_admin_message
from handlers.expert_handlers import handle_expert_message
from handlers.tracking_handlers import handle_tracking_message


# -----------------------------
# Role + State Based Router
# -----------------------------
def route_message(chat_id: int, message: str, role: str = "USER", state: str = "MAIN_MENU") -> str:
    """
    Route message based on user role and conversation state.

    Args:
        chat_id: Telegram/Bale user ID
        message: Incoming message text
        role: USER | ADMIN | EXPERT
        state: Conversation state (MAIN_MENU, TRACKING, CHAT, etc.)

    Returns:
        Response string from appropriate handler
    """

    # -----------------------------
    # ADMIN ROUTING (highest priority)
    # -----------------------------
    if role == "ADMIN":
        return handle_admin_message(
            chat_id=chat_id,
            message=message,
            state=state
        )

    # -----------------------------
    # EXPERT ROUTING
    # -----------------------------
    if role == "EXPERT":
        return handle_expert_message(
            chat_id=chat_id,
            message=message,
            state=state
        )

    # -----------------------------
    # STATE-BASED ROUTING (USER)
    # -----------------------------

    # Tracking has highest priority in USER flow
    if state == "TRACKING":
        tracking_response = handle_tracking_message(chat_id, message)
        if tracking_response:
            return tracking_response

    # Expert chat state
    if state == "CHAT_WITH_EXPERT":
        return handle_expert_message(chat_id, message)

    # Request creation flow
    if state == "CREATING_REQUEST":
        return handle_user_message(
            chat_id=chat_id,
            message=message,
            state=state
        )

    # Default → User handler (main menu / general flow)
    return handle_user_message(
        chat_id=chat_id,
        message=message,
        state=state
    )
