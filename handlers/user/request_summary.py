"""
handlers/user/request_summary.py

Build and show request summary.
"""

from user_state import get_data

from ticket_formatter import (
    SERVICE_NAMES,
    SUB_SERVICE_NAMES,
)


# ----------------------------------
# Persian Labels
# ----------------------------------
FIELD_LABELS = {

    "service": "خدمت",

    "sub_service": "زیرخدمت",

    "request_number": "شماره تقاضا",

    "computer_code": "رمز رایانه",

    "bill_id": "شناسه قبض",

    "national_code": "کد ملی",

    "mobile": "شماره همراه",

    "subscription": "شماره اشتراک",

    "meter_serial": "سریال کنتور",

    "full_name": "نام و نام خانوادگی",

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

    # ----------------------------------
    # Service
    # ----------------------------------

    service = data.get("service")

    if service:

        lines.append(
            f"🔹 خدمت: {SERVICE_NAMES.get(service, service)}"
        )

    # ----------------------------------
    # Sub Service
    # ----------------------------------

    sub_service = data.get("sub_service")

    if sub_service:

        lines.append(
            f"🔹 زیرخدمت: {SUB_SERVICE_NAMES.get(sub_service, sub_service)}"
        )

    # ----------------------------------
    # Other Fields
    # ----------------------------------

    for key, value in data.items():

        if key in (
            "service",
            "sub_service",
        ):
            continue

        if value in (
            None,
            "",
        ):
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
