"""
handlers/tracking_handlers.py

Request tracking handler.
"""

from database import (
    get_request_by_tracking,
    get_messages,
)

from ticket_formatter import (
    format_user_history,
)

from user_state import (
    set_state,
    clear_state,
)


# -----------------------------
# Start Tracking
# -----------------------------
def start_tracking(
    chat_id: int,
) -> dict:
    """
    Ask user to enter tracking code.
    """

    set_state(
        chat_id,
        "WAITING_TRACKING_CODE",
    )

    return {

        "text":
            "🎫 لطفاً کد پیگیری درخواست را وارد کنید.",

    }


# -----------------------------
# Handle Tracking Code
# -----------------------------
def handle_tracking(
    chat_id: int,
    tracking_code: str,
) -> dict:
    """
    Return request history by tracking code.
    """

    tracking_code = tracking_code.strip()

    # بعد از دریافت کد، از حالت انتظار خارج شو
    clear_state(chat_id)

    # -------------------------
    # Find Request
    # -------------------------

    request = get_request_by_tracking(
        tracking_code,
    )

    if request is None:

        return {

            "text":
                "❌ درخواستی با این کد پیگیری یافت نشد.",

        }

    # -------------------------
    # Ownership Check
    # -------------------------

    if request["chat_id"] != chat_id:

        return {

            "text":
                "⛔ این کد پیگیری متعلق به شما نیست.",

        }

    # -------------------------
    # Load Messages
    # -------------------------

    messages = get_messages(
        tracking_code,
    )

    # -------------------------
    # Build Response
    # -------------------------

    text = format_user_history(

        tracking=tracking_code,

        status=request["status"],

        messages=messages,

    )

    return {

        "text": text,

    }
