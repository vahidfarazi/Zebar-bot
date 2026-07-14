"""
handlers/user/description_handler.py

Handle optional request description and final confirmation.
"""

from user_state import (
    get_data,
    update_data,
    set_state,
    reset,
)

from menus import (
    MAIN_MENU,
    DESCRIPTION_MENU,
    CONFIRM_MENU,
)

from request_service import (
    create_request,
)

from handlers.user.request_summary import (
    show_summary,
)

from handlers.user.edit_request import (
    edit_menu,
    start_edit,
)


MAX_DESCRIPTION = 300


# =================================================
# Description
# =================================================

def handle_description(
    chat_id: int,
    message: str,
):

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
                    (
                        f"❌ توضیحات نباید بیشتر از "
                        f"{MAX_DESCRIPTION} کاراکتر باشد."
                    ),

                "keyboard":
                    DESCRIPTION_MENU,

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


    result = show_summary(
        chat_id,
    )


    result["keyboard"] = CONFIRM_MENU


    return result



# =================================================
# Confirm
# =================================================

def handle_confirm(
    chat_id: int,
    message: str,
):


    if message == "✏️ ویرایش درخواست":

        return edit_menu(
            chat_id,
        )


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


    if message == "❌ انصراف":

        reset(
            chat_id,
        )


        return {

            "text":
                "ثبت درخواست لغو شد.",

            "keyboard":
                MAIN_MENU,

        }



    if message != "✅ ثبت نهایی":

        return {

            "text":
                "لطفاً یکی از گزینه‌های موجود را انتخاب کنید.",

            "keyboard":
                CONFIRM_MENU,

        }



    data = get_data(
        chat_id,
    )


    result = create_request(
        chat_id,
        data,
    )


    reset(
        chat_id,
    )


    return {

        "text":
            result.get(
                "user_message",
                "درخواست ثبت شد.",
            ),

        "keyboard":
            MAIN_MENU,

    }
