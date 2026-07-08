"""
main_runner.py

Core runtime processor for Azarakhsh system.
"""

import traceback

from router import route_message
from callback_handler import handle_callback

from logger import (
    log_error,
    log_info,
)

from database import (
    create_user,
    get_expert,
    is_admin,
)

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
                chat_id=chat_id,
                text=result.get("text", ""),
                keyboard=result.get("keyboard"),
            )

        else:

            send_message(
                chat_id=chat_id,
                text=str(result),
            )

        log_info(
            "runner",
            "process_update",
            str(chat_id),
        )

    except Exception as e:

        traceback.print_exc()

        log_error(
            "runner",
            "process_update",
            str(e),
        )

        try:

            send_message(
                chat_id=chat_id,
                text="خطایی رخ داد.",
            )

        except Exception:

            traceback.print_exc()


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

        # -----------------------------
        # Detect Role
        # -----------------------------
        role = "USER"

        if is_admin(chat_id):

            role = "ADMIN"

        elif get_expert(chat_id):

            role = "EXPERT"

        process_update(
            chat_id,
            text,
            role,
        )

    except Exception as e:

        traceback.print_exc()

        log_error(
            "runner",
            "handle_update",
            str(e),
        )
