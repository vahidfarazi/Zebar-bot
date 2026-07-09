"""
ticket_formatter.py

Request text formatter.
"""

FIELD_NAMES = {

    "request_number": "شماره تقاضا",

    "computer_code": "رمز رایانه",

    "bill_id": "شناسه قبض",

    "national_code": "کد ملی",

    "mobile": "شماره همراه",

    "subscription": "اشتراک",

    "meter_serial": "سریال کنتور",

}


SERVICE_NAMES = {

    "NEW_CONNECTION":
        "نصب انشعاب جدید",

    "AFTER_SALES":
        "خدمات پس از فروش",

    "METER_TEST":
        "بازرسی و تست کنتور",

    "BILL_INQUIRY":
        "بررسی قبض برق",

}


SUB_SERVICE_NAMES = {

    "UNKNOWN":
        "نامشخص",

    "SERVICE_FIX":
        "اصلاح سرویس",

    "REINSTALL":
        "نصب مجدد",

    "RELOCATION":
        "تغییر مکان",

    "CHANGE_NAME":
        "تغییر نام",

    "AMPERAGE":
        "تبدیل آمپراژ",

    "TEMP_REMOVE":
        "جمع‌آوری موقت",

    "PERMANENT_REMOVE":
        "جمع‌آوری دائم",

}


# -----------------------------
# Request Body
# -----------------------------
def format_request(
    data: dict,
) -> str:

    lines = []

    service = data.get("service")

    if service:

        lines.append(
            f"خدمت: {SERVICE_NAMES.get(service, service)}"
        )

    sub = data.get("sub_service")

    if sub:

        lines.append(
            f"زیرخدمت: {SUB_SERVICE_NAMES.get(sub, sub)}"
        )

    lines.append("")

    for key, title in FIELD_NAMES.items():

        value = data.get(key)

        if value:

            lines.append(
                f"{title}: {value}"
            )

    return "\n".join(lines)


# -----------------------------
# Expert Message
# -----------------------------
def format_expert(
    tracking: str,
    chat_id: int,
    data: dict,
) -> str:

    return "\n".join(

        [

            "📩 درخواست جدید",

            "",

            f"🎫 {tracking}",

            "",

            format_request(data),

            "",

            f"👤 شناسه بله: {chat_id}",

        ]

    )


# -----------------------------
# User History
# -----------------------------
def format_user_history(
    tracking: str,
    status: str,
    messages: list[dict],
) -> str:

    status_map = {

        "OPEN": "در حال بررسی",

        "ANSWERED": "پاسخ داده شده",

        "CLOSED": "بسته شده",

    }

    lines = [

        "📋 پیگیری درخواست",

        "",

        f"🎫 {tracking}",

        "",

        f"📌 وضعیت: {status_map.get(status, status)}",

        "",

        "━━━━━━━━━━━━━━",

    ]

    for item in messages:

        if item["sender_type"] == "USER":

            lines.extend([

                "",

                "👤 درخواست",

                "",

                item["message"],

                "",

                "━━━━━━━━━━━━━━",

            ])

        else:

            lines.extend([

                "",

                "👨‍💼 پاسخ کارشناس",

                "",

                item["message"],

                "",

                "━━━━━━━━━━━━━━",

            ])

    return "\n".join(lines)


# -----------------------------
# Success Message
# -----------------------------
def format_success(
    tracking: str,
) -> str:

    return (

        "✅ درخواست شما با موفقیت ثبت شد."

        "\n\n"

        "کد پیگیری شما:"

        "\n"

        f"{tracking}"

        "\n\n"

        "این کد را برای پیگیری نزد خود نگه دارید."

    )
