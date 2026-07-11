"""
handlers/user/request_summary.py

Build and show request summary.
"""

from user_state import get_data


# ----------------------------------
# Persian Labels
# ----------------------------------
FIELD_LABELS = {

    "service": "خدمت",

    "full_name": "نام و نام خانوادگی",

    "mobile": "شماره همراه",

    "national_code": "کد ملی",

    "bill_id": "شناسه قبض",

    "computer_no": "رمز رایانه",

    "meter_no": "شماره کنتور",

    "address": "نشانی",

    "description": "توضیحات تکمیلی",

}


# ----------------------------------
# Build Summary Text
# ----------------------------------
def build_summary(
    chat_id: int,
) -> str:

    data = get_data(chat_id)

    lines = [

        "📋 خلاصه درخواست",
        "",
    ]

    for key, value in data.items():

        if value in (None, ""):
            continue

        title = FIELD_LABELS.get(
            key,
            key,
        )

        lines.append(
            f"🔹 {title}: {value}"
        )

    return "\n".join(lines)


# ----------------------------------
# Summary Response
# ----------------------------------
def show_summary(
    chat_id: int,
):

    return {

        "text": (
            build_summary(chat_id)
            + "\n\n"
            + "در صورت تأیید، درخواست شما ثبت خواهد شد."
        ),

        "keyboard": [

            ["✅ ثبت نهایی"],

            ["✏️ ویرایش درخواست"],

            ["❌ انصراف"],

        ],

    }
