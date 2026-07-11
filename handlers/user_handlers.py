"""
handlers/user_handlers.py

Main user router.
"""

from handlers.user.main_menu import handle_main_menu
from handlers.user.request_menu import handle_request_menu
from handlers.user.form_handler import handle_form

from handlers.user.description_handler import (
    handle_description,
    handle_confirm,
)

from handlers.tracking_handlers import (
    start_tracking,
    handle_tracking,
)

from user_state import get_state


# -------------------------------------------------
# Handle User
# -------------------------------------------------
def handle_user_message(
    chat_id: int,
    message: str,
):

    state = get_state(chat_id)

    # -----------------------------------------
    # Tracking
    # -----------------------------------------

    if state == "WAITING_TRACKING_CODE":

        return handle_tracking(
            chat_id,
            message,
        )

    # -----------------------------------------
    # Optional Description
    # -----------------------------------------

    if state == "WAITING_DESCRIPTION":

        return handle_description(
            chat_id,
            message,
        )

    # -----------------------------------------
    # Final Confirmation
    # -----------------------------------------

    if state == "WAITING_CONFIRM":

        return handle_confirm(
            chat_id,
            message,
        )

    # -----------------------------------------
    # Form
    # -----------------------------------------

    if state:

        return handle_form(
            chat_id,
            message,
            state,
        )

    # -----------------------------------------
    # Main Menu
    # -----------------------------------------

    if (
        message == "/start"
        or message == "🏠 منوی اصلی"
    ):

        return handle_main_menu(
            chat_id,
        )

    # -----------------------------------------
    # Request Menu
    # -----------------------------------------

    request_result = handle_request_menu(
        chat_id,
        message,
    )

    if request_result["text"] != "لطفاً فقط از گزینه‌های موجود استفاده کنید.":

        return request_result

    # -----------------------------------------
    # Tracking
    # -----------------------------------------

    if message == "📋 پیگیری درخواست":

        return start_tracking(
            chat_id,
        )

    # -----------------------------------------
    # Invalid
    # -----------------------------------------

    return {

        "text":
            "لطفاً فقط از دکمه‌های موجود استفاده کنید.",

    }
