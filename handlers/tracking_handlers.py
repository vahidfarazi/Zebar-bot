"""
handlers/tracking_handlers.py

Request tracking handler.
"""

from database import (
    get_request_by_tracking,
    get_messages,
    get_history,
    get_last_message,
    count_messages,
)

from ticket_formatter import (
    format_user_history,
)

from working_hours import (
    calculate_sla,
)

from user_state import (
    set_state,
    clear_state,
)

from validators import (
    normalize_digits,
)


# ----------------------------------
# Start Tracking
# ----------------------------------

def start_tracking(
    chat_id: int,
) -> dict:

    set_state(
        chat_id,
        "WAITING_TRACKING_CODE",
    )

    return {

        "text":
            "🎫 لطفاً کد پیگیری درخواست را وارد کنید.",

    }


# ----------------------------------
# Handle Tracking
# ----------------------------------

def handle_tracking(
    chat_id: int,
    tracking_code: str,
) -> dict:

    # Normalize Persian/Arabic digits
    tracking_code = normalize_digits(
        tracking_code.strip()
    )

    clear_state(chat_id)


    request = get_request_by_tracking(
        tracking_code,
    )


    if request is None:

        return {

            "text":
                "❌ درخواستی با این کد پیگیری یافت نشد.",

        }


    if request["chat_id"] != chat_id:

        return {

            "text":
                "⛔ این کد پیگیری متعلق به شما نیست.",

        }


    messages = get_messages(
        tracking_code,
    )


    history = get_history(
        tracking_code,
    )


    last_message = get_last_message(
        tracking_code,
    )


    message_count = count_messages(
        tracking_code,
    )


    sla = None


    if request.get("closed_at"):

        sla = calculate_sla(
            request["created_at"],
            request["closed_at"],
        )


    # --------------------------------
    # Format Tracking Result
    # --------------------------------

    text = format_user_history(

        request=request,

        messages=messages,

        history=history,

    )


    return {

        "text": text,

    }
