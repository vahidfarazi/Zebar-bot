"""
handlers/user_handlers.py

Main user router.
"""

from handlers.user.main_menu import handle_main_menu
from handlers.user.request_menu import handle_request_menu
from handlers.user.form_handler import handle_form

from handlers.user.edit_request import (
    save_edit,
    start_edit,
)

from handlers.user.request_summary import (
    show_summary,
)

from handlers.tracking_handlers import (
    start_tracking,
    handle_tracking,
)

from user_state import (
    get_state,
    set_state,
)


# -----------------------------
# Handle User
# -----------------------------
def handle_user_message(
    chat_id: int,
    message: str,
):

    state = get_state(chat_id)

    # -----------------------------
    # Tracking Mode
    # -----------------------------
    if state == "WAITING_TRACKING_CODE":

        return handle_tracking(
            chat_id,
            message,
        )

    # -----------------------------
    # Edit Menu
    # -----------------------------
    if state == "WAITING_EDIT_MENU":

        if message == "✅ بازگشت به خلاصه":

            set_state(
                chat_id,
                "WAITING_CONFIRM",
            )

            return show_summary(
                chat_id,
            )

        return start_edit(
            chat_id,
            message,
        )

    # -----------------------------
    # Edit Field
    # -----------------------------
    if state and state.startswith("EDIT_"):

        return save_edit(
            chat_id,
            state,
            message,
        )

    # -----------------------------
    # Form Mode
    # -----------------------------
    if state:

        return handle_form(
            chat_id,
            message,
            state,
        )

    # -----------------------------
    # Main Menu
    # -----------------------------
    if (
        message == "/start"
        or message == "🏠 منوی اصلی"
    ):

        return handle_main_menu(
            chat_id,
        )

    # -----------------------------
    # Request Menu
    # -----------------------------
    request_result = handle_request_menu(
        chat_id,
        message,
    )

    if request_result["text"] != "لطفاً فقط از گزینه‌های موجود استفاده کنید.":

        return request_result

    # -----------------------------
    # Tracking
    # -----------------------------
    if message == "📋 پیگیری درخواست":

        return start_tracking(
            chat_id,
        )

    # -----------------------------
    # Invalid
    # -----------------------------
    return {

        "text":
            "لطفاً فقط از دکمه‌های موجود استفاده کنید.",

    }
