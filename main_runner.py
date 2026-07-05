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


def process_update(
    chat_id: int,
    message: str,
    role: str = "USER",
) -> str:

    try:

        create_user(chat_id)

        response = route_message(
            chat_id,
            message,
            role,
        )

        send_message(
            chat_id,
            response,
        )

        log_info(
            "runner",
            "process_update",
            str(chat_id),
        )

        return response

    except Exception as e:

        log_error(
            "runner",
            "process_update",
            str(e),
        )

        send_message(
            chat_id,
            "خطایی رخ داد",
        )

        return "خطایی رخ داد"


def handle_update(update: dict) -> None:

    try:

        message = update.get("message", {})

        chat = message.get("chat", {})

        chat_id = chat.get("id")
        text = message.get("text", "")

        role = "USER"

        if chat_id is None:
            return

        if not text:
            return

        if not can_create_request():
            send_message(
                chat_id,
                "سیستم در حال حاضر در دسترس نیست",
            )
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
