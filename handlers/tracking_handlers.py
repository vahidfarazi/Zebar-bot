"""
handlers/tracking_handler.py

Request tracking handler.
"""

from database import (
    get_request_by_tracking,
    get_messages,
)

from ticket_formatter import (
    format_user_history,
)


# -----------------------------
# Handle Tracking
# -----------------------------
def handle_tracking(
    chat_id: int,
    tracking_code: str,
) -> dict:
    """
    Return request history by tracking code.
    """

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
    # Load Conversation
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
