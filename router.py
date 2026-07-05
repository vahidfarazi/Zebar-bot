"""
router.py

Central message router for Azarakhsh.
"""

from handlers.user_handlers import handle_user_message
from handlers.admin_handlers import handle_admin_message
from handlers.expert_handlers import handle_expert_message


# -----------------------------
# Main Router
# -----------------------------
def route_message(
    chat_id: int,
    message: str,
    role: str = "USER",
):
    """
    Route incoming message.
    """

    if not isinstance(message, str):
        message = ""

    message = message.strip()

    # -----------------------------
    # Admin
    # -----------------------------
    if role == "ADMIN":

        return handle_admin_message(
            chat_id,
            message,
        )

    # -----------------------------
    # Expert
    # -----------------------------
    if role == "EXPERT":

        return handle_expert_message(
            chat_id,
            message,
        )

    # -----------------------------
    # User
    # -----------------------------
    return handle_user_message(
        chat_id,
        message,
    )
