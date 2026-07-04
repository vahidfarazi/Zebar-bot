"""
handlers.py

Responsible for receiving user messages,
routing them to services, and returning responses.

NO business logic allowed here.
"""

from logger import log_info, log_error
from validators import validate_tracking_code
from tracking import generate_tracking_code
from working_hours import can_create_request
from database import fetch_one


# -----------------------------
# Simple Router (placeholder)
# -----------------------------
def handle_message(chat_id: int, message: str) -> str:
    """
    Main entry for all incoming messages.
    """

    try:
        log_info("handlers", "receive_message", f"chat_id={chat_id}")

        # -----------------------------
        # Tracking search
        # -----------------------------
        if validate_tracking_code(message):
            request = fetch_one(
                "SELECT * FROM requests WHERE tracking_code = ?",
                (message,),
            )

            if request:
                return f"درخواست شما یافت شد: {request['status']}"
            else:
                return "درخواستی با این شماره رهگیری یافت نشد."

        # -----------------------------
        # Create request (simplified)
        # -----------------------------
        if message == "ثبت درخواست":
            if not can_create_request():
                return "در حال حاضر امکان ثبت درخواست وجود ندارد."

            tracking = generate_tracking_code()
            return f"درخواست شما ثبت شد.\nکد رهگیری:\n{tracking}"

        # -----------------------------
        # Default response
        # -----------------------------
        return "پیام شما دریافت شد."

    except Exception as e:
        log_error("handlers", "handle_message_error", str(e))
        return "خطایی در پردازش پیام رخ داد."
