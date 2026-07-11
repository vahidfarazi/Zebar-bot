"""
handlers/user/edit_request.py
"""

from user_state import (
    get_data,
    set_state,
    update_data,
)

from handlers.user.request_summary import show_summary

EDIT_FIELDS = {

    "⚡ رمز رایانه": "computer_code",

    "🧾 شناسه قبض": "bill_id",

    "🪪 کد ملی": "national_code",

    "📱 شماره همراه": "mobile",

    "📝 توضیحات": "description",

}

FIELD_TITLES = {

    "computer_code": "رمز رایانه",

    "bill_id": "شناسه قبض",

    "national_code": "کد ملی",

    "mobile": "شماره همراه",

    "description": "توضیحات تکمیلی",

}


def edit_menu(chat_id):

    data = get_data(chat_id)

    keyboard = []

    if data.get("computer_code"):
        keyboard.append(["⚡ رمز رایانه"])

    if data.get("bill_id"):
        keyboard.append(["🧾 شناسه قبض"])

    if data.get("national_code"):
        keyboard.append(["🪪 کد ملی"])

    if data.get("mobile"):
        keyboard.append(["📱 شماره همراه"])

    keyboard.append(["📝 توضیحات"])

    keyboard.append(["⬅️ بازگشت"])

    return {

        "text": "کدام بخش را می‌خواهید ویرایش کنید؟",

        "keyboard": keyboard,

    }


def start_edit(chat_id, message):

    if message == "⬅️ بازگشت":

        return show_summary(chat_id)

    field = EDIT_FIELDS.get(message)

    if not field:

        return {

            "text": "لطفاً یکی از گزینه‌های موجود را انتخاب کنید.",

        }

    set_state(

        chat_id,

        f"EDIT_{field.upper()}",

    )

    return {

        "text": f"{FIELD_TITLES[field]} جدید را وارد کنید.",

    }


def save_edit(chat_id, state, message):

    field = state.replace(

        "EDIT_",

        "",

    ).lower()

    update_data(

        chat_id,

        field,

        message,

    )

    set_state(

        chat_id,

        "WAITING_CONFIRM",

    )

    return show_summary(chat_id)
