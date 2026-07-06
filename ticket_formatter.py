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

}


SERVICE_NAMES = {

    "NEW_CONNECTION":
        "نصب انشعاب جدید",

    "AFTER_SALES":
        "خدمات پس از فروش",

    "METER_TEST":
        "بازرسی و تست کنتور",

    "BILL":
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

            f"👤 شناسه مشترک: {chat_id}",

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

    lines = [

        f"🎫 {tracking}",

        "",

        f"وضعیت: {status}",

        "",

        "━━━━━━━━━━━━",

    ]

    for item in messages:

        sender = item["sender_type"]

        if sender == "USER":

            prefix = "👤"

        else:

            prefix = "👨‍💼"

        lines.append("")

        lines.append(

            f"{prefix} {item['message']}"

        )

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
