"""
main_runner.py

Core runtime processor for Azarakhsh system.
"""

from router import route_message

from logger import (
    log_error,
    log_info,
)

from database import create_user

from bale_client import send_message

# این را بعداً می‌سازیم
from expert_handlers import handle_callback


# -----------------------------
# Process Update
# -----------------------------
def process_update(
    chat_id: int,
    message: str,
    role: str = "USER",
) -> None:

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
                result.get("keyboard"),
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

        print("CHAT ID:", chat_id)

        if not chat_id:

            return

        text = message.get("text", "")

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
