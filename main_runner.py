"""
main_runner.py

Core runtime processor for Azarakhsh system.
"""

from router import route_message
from callback_handler import handle_callback

from logger import (
    log_error,
    log_info,
)

from database import create_user

from bale_client import send_message


# -----------------------------
# Process Update
# -----------------------------
def process_update(
    chat_id: int,
    message: str,
    role: str = "USER",
) -> None:
    """
    Process incoming message.
    """

    try:

        create_user(chat_id)

        result = route_message(
            chat_id,
            message,
            role,
        )

        if result is None:
            return

        if isinstance(result, dict):

            send_message(
                chat_id,
                result.get("text", ""),
                keyboard=result.get("keyboard"),
            )

        else:

            send_message(
                chat_id,
                str(result),
            )

        log_info(
            "runner",
            "process_update",
            str(chat_id),
        )

    except Exception as e:

        log_error(
            "runner",
            "process_update",
            str(e),
        )

        send_message(
            chat_id,
            "خطایی رخ داد.",
        )


# -----------------------------
# Handle Incoming Update
# -----------------------------
def handle_update(
    update: dict,
) -> None:
    """
    Entry point.
    """

    try:

        print("========== UPDATE ==========")
        print(update)
        print("============================")

        # -----------------------------
        # Callback Query
        # -----------------------------
        callback = update.get("callback_query")

        if callback:

            handle_callback(callback)
            return

        # -----------------------------
        # Message
        # -----------------------------
        message = update.get("message", {})

        chat = message.get("chat", {})

        chat_id = chat.get("id")

        text = message.get("text", "")

        if not chat_id:
            return

        process_update(
            chat_id,
            text,
        )

    except Exception as e:

        log_error(
            "runner",
            "handle_update",
            str(e),
        )
