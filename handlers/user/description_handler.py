"""
handlers/user/description_handler.py

Handle optional request description.
"""

from user_state import (
    get_data,
    update_data,
    set_state,
    reset,
)

from menus import MAIN_MENU
from request_service import create_request

from handlers.user.request_summary import show_summary
from handlers.user.edit_request import (
    edit_menu,
    start_edit,
)


MAX_DESCRIPTION = 300


def handle_description(
    chat_id: int,
    message: str,
):

    # -----------------------------
    # بدون توضیح
    # -----------------------------

    if message == "⏭ بدون توضیح":

        update_data(
            chat_id,
            "description",
            "",
        )

    else:

        message = message.strip()

        if len(message) > MAX_DESCRIPTION:

            return {

                "text":
                    f"❌ توضیحات نباید بیشتر از {MAX_DESCRIPTION} کاراکتر باشد.",

                "keyboard": [
                    ["⏭ بدون توضیح"],
                    ["❌ انصراف"],
                ],

            }

        update_data(
            chat_id,
            "description",
            message,
        )

    set_state(
        chat_id,
        "WAITING_CONFIRM",
    )

    return show_summary(chat_id)


def handle_confirm(
    chat_id: int,
    message: str,
):

    # -----------------------------
    # Edit Menu
    # -----------------------------

    if message == "✏️ ویرایش درخواست":

        return edit_menu(chat_id)

    # -----------------------------
    # Edit Field
    # -----------------------------

    if message.startswith(

        (
            "⚡",
            "🧾",
            "🪪",
            "📱",
            "📝",
            "⬅️",
        )

    ):

        return start_edit(
            chat_id,
            message,
        )

    # -----------------------------
    # Cancel
    # -----------------------------

    if message == "❌ انصراف":

        reset(chat_id)

        return {

            "text": "ثبت درخواست لغو شد.",

            "keyboard": MAIN_MENU,

        }

    # -----------------------------
    # Invalid
    # -----------------------------

    if message != "✅ ثبت نهایی":

        return {

            "text":
                "لطفاً یکی از گزینه‌های موجود را انتخاب کنید.",

        }

    # -----------------------------
    # Final Save
    # -----------------------------

    data = get_data(chat_id)

    result = create_request(
        chat_id,
        data,
    )

    reset(chat_id)

    return {

        "text": result["user_message"],

        "keyboard": MAIN_MENU,

    }
