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

from menus import (
    MAIN_MENU,
    REQUEST_MENU,
)

from request_service import create_request


MAX_DESCRIPTION = 300


# -----------------------------
# عنوان فیلدها
# -----------------------------
FIELD_TITLES = {
    "bill_id": "شناسه قبض",
    "meter_serial": "شماره سریال کنتور",
    "computer_code": "رمز رایانه",
    "national_code": "کد ملی",
    "mobile": "شماره همراه",
    "phone": "تلفن ثابت",
    "address": "نشانی",
    "tracking_code": "کد رهگیری",
}


# -----------------------------
# Summary Builder
# -----------------------------
def build_summary(data: dict) -> str:

    lines = []

    lines.append("📋 خلاصه درخواست")
    lines.append("")

    service = data.get("service")

    if service:
        lines.append(f"🔹 خدمت: {service}")
        lines.append("")

    for key, value in data.items():

        if key in (
            "service",
            "description",
        ):
            continue

        if value in (
            None,
            "",
        ):
            continue

        title = FIELD_TITLES.get(
            key,
            key,
        )

        lines.append(f"• {title}: {value}")

    description = data.get("description")

    if description:

        lines.append("")
        lines.append("📝 توضیحات تکمیلی:")
        lines.append(description)

    lines.append("")
    lines.append("در صورت تأیید، درخواست ثبت خواهد شد.")

    return "\n".join(lines)


# -----------------------------
# Description Step
# -----------------------------
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

                "text": (
                    f"❌ توضیحات نباید بیشتر از "
                    f"{MAX_DESCRIPTION} کاراکتر باشد."
                ),

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

        "text": build_summary(data),

        "keyboard": [

            ["✅ ثبت نهایی"],

            ["✏️ ویرایش درخواست"],

            ["❌ انصراف"],

        ],

    }


# -----------------------------
# Final Confirmation
# -----------------------------
def handle_confirm(
    chat_id: int,
    message: str,
):

    # -------------------------
    # Cancel
    # -------------------------
    if message == "❌ انصراف":

        reset(chat_id)

        return {

            "text": "ثبت درخواست لغو شد.",

            "keyboard": MAIN_MENU,

        }

    # -------------------------
    # Edit
    # -------------------------
    if message == "✏️ ویرایش درخواست":

        reset(chat_id)

        return {

            "text": (
                "درخواست قبلی لغو شد.\n\n"
                "لطفاً خدمت موردنظر را دوباره انتخاب کنید."
            ),

            "keyboard": REQUEST_MENU,

        }

    # -------------------------
    # Invalid
    # -------------------------
    if message != "✅ ثبت نهایی":

        return {

            "text":
                "لطفاً یکی از گزینه‌های موجود را انتخاب کنید.",

            "keyboard": [

                ["✅ ثبت نهایی"],

                ["✏️ ویرایش درخواست"],

                ["❌ انصراف"],

            ],

        }

    # -------------------------
    # Save Request
    # -------------------------
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
