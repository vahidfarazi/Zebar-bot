"""
ticket_formatter.py

Formats request data for database,
expert group and user.
"""

FIELD_NAMES = {

    "request_number": "شماره تقاضا",

    "computer_code": "رمز رایانه",

    "bill_id": "شناسه قبض",

    "national_code": "کد ملی",

    "mobile": "شماره تلفن همراه",

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
        "نوع درخواست مشخص نیست",

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
# Database Text
# -----------------------------
def format_database(data: dict) -> str:

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

    for key, title in FIELD_NAMES.items():

        if key in data:

            lines.append(
                f"{title}: {data[key]}"
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

    text = []

    text.append("📩 درخواست جدید")

    text.append("")

    text.append(
        f"کد پیگیری: {tracking}"
    )

    text.append(
        f"کاربر: {chat_id}"
    )

    text.append("")

    text.append(
        format_database(data)
    )

    return "\n".join(text)


# -----------------------------
# User Success
# -----------------------------
def format_success(
    tracking: str,
) -> str:

    return (
        "✅ درخواست شما با موفقیت ثبت شد.\n\n"
        f"کد پیگیری:\n{tracking}"
    )
