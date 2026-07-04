"""
user_handlers.py

Handles all USER role interactions.
Acts as bridge between router and services.
"""

from request_service import create_request, reply_request
from logger import log_info
from messages import REQUEST_CREATED, INVALID_INPUT, GENERAL_ERROR


# -----------------------------
# Handle User Message
# -----------------------------
def handle_user_message(chat_id: int, message: str) -> str:
    """
    Process user messages.
    """

    try:
        message = message.strip()

        # -------------------------
        # Create Request Command
        # Example: /new title|description
        # -------------------------
        if message.startswith("/new"):
            parts = message.replace("/new", "").strip().split("|")

            if len(parts) < 2:
                return INVALID_INPUT

            title = parts[0].strip()
            description = parts[1].strip()

            result = create_request(chat_id, title, description)

            if result["success"]:
                log_info("user_handlers", "create_request", f"user={chat_id}")
                return f"{REQUEST_CREATED}\n\nTracking:\n{result['tracking_code']}"

            return result.get("message", GENERAL_ERROR)

        # -------------------------
        # Default fallback (chat message)
        # -------------------------
        result = reply_request(
            request_id=chat_id,  # MVP simplification (will be replaced with state system)
            sender_type="USER",
            message=message,
        )

        if result["success"]:
            return "پیام شما ثبت شد."

        return result.get("message", GENERAL_ERROR)

    except Exception as e:
        log_info("user_handlers", "error", str(e))
        return GENERAL_ERROR
