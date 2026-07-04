"""
main_runner.py

Core runtime processor for Azarakhsh system.
Handles incoming updates from Bale and routes responses.
"""

from router import route_message
from logger import log_error, log_info
from database import create_user
from working_hours import can_create_request

from bale_client import send_message


# -----------------------------
# Process Update
# -----------------------------
def process_update(
    chat_id: int,
    message: str,
    role: str = "USER",
) -> str:
    """
    Process incoming message and send response to Bale.
    """

    try:

        # Ensure user exists
        create_user(chat_id)

        # Route message
        response = route_message(
            chat_id,
            message,
            role,
        )

        # Send response to Bale
        send_message(
            chat_id,
            response,
        )

        log_info(
            "runner",
            "process_update",
            f"{chat_id}",
        )

        return response

    except Exception as e:

        log_error(
            "runner",
            "process_update",
            str(e),
        )

        error_msg = "خطایی رخ داد"

        send_message(
            chat_id,
            error_msg,
        )

        return error_msg


# -----------------------------
# Incoming Update Handler (entry point)
# -----------------------------
def handle_update(update: dict) -> None:
    """
    Entry point for webhook / polling updates.
    """

    try:

        message = update.get("message", {})

        chat_id = message.get("chat_id")
        text = message.get("text", "")

        role = message.get("role", "USER")

        if not chat_id or not text:
            return

        # Optional: block if system not allowed
        if not can_create_request():
            send_message(chat_id, "سیستم در حال حاضر در دسترس نیست")
            return

        process_update(
            chat_id,
            text,
            role,
        )

    except Exception as e:

        log_error(
            "runner",
            "handle_update",
            str(e),
        )
