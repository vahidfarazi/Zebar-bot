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


MAX_DESCRIPTION = 300


def build_summary(data: dict) -> str:
    """
    Build request summary.
    """

    text = "📋 خلاصه درخواست\n\n"

    service = data.get("service")
    if service:
        text += f"🔹 خدمت: {service}\n"

    for key, value in data.items():

        if key == "service":
            continue

        if key == "description":
            continue

        text += f"• {key}: {value}\n"

    description = data.get("description")

    if description:

        text += "\n📝 توضیحات تکمیلی:\n"
        text += description

    return text


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

    data = get_data(chat_id)

    set_state(
        chat_id,
        "WAITING_CONFIRM",
    )

    return {

        "text": (
            build_summary(data)
            + "\n\n"
            + "در صورت تأیید، درخواست ثبت خواهد شد."
        ),

        "keyboard": [

            ["✅ ثبت نهایی"],

            ["✏️ ویرایش درخواست"],

            ["❌ انصراف"],

        ],

    }


def handle_confirm(
    chat_id: int,
    message: str,
):

    if message == "❌ انصراف":

        reset(chat_id)

        return {

            "text": "ثبت درخواست لغو شد.",

            "keyboard": MAIN_MENU,

        }

    if message == "✏️ ویرایش درخواست":

        reset(chat_id)

        return {

            "text": "لطفاً درخواست را دوباره ثبت کنید.",

            "keyboard": MAIN_MENU,

        }

    if message != "✅ ثبت نهایی":

        return {

            "text":
                "لطفاً یکی از گزینه‌های موجود را انتخاب کنید.",

        }

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
