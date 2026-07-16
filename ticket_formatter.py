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
    "NEW_CONNECTION": "نصب انشعاب جدید",
    "AFTER_SALES": "خدمات پس از فروش",
    "METER_TEST": "بازرسی و تست کنتور",
    "BILL_INQUIRY": "بررسی قبض برق",
}

SUB_SERVICE_NAMES = {
    "UNKNOWN": "نامشخص",
    "SERVICE_FIX": "اصلاح سرویس",
    "REINSTALL": "نصب مجدد",
    "RELOCATION": "تغییر مکان",
    "CHANGE_NAME": "تغییر نام",
    "AMPERAGE": "تبدیل آمپراژ",
    "TEMP_REMOVE": "جمع‌آوری موقت",
    "PERMANENT_REMOVE": "جمع‌آوری دائم",
}

STATUS_NAMES = {
    "OPEN": "در حال بررسی",
    "PENDING": "در انتظار پاسخ",
    "ANSWERED": "پاسخ داده شده",
    "TRANSFERRED": "ارجاع شده",
    "CLOSED": "بسته شده",
}


# ---------------------------------------------------
# Request Body
# ---------------------------------------------------

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

    description = data.get("description")

    if description:
        lines.extend(
            [
                "",
                "توضیحات تکمیلی:",
                description,
            ]
        )

    return "\n".join(lines)



# ---------------------------------------------------
# Summary
# ---------------------------------------------------

def format_summary(
    data: dict,
) -> str:

    lines = [
        "📋 خلاصه درخواست",
        "",
    ]

    service = data.get("service")

    if service:
        lines.append(
            f"🔹 خدمت: {SERVICE_NAMES.get(service, service)}"
        )

    sub = data.get("sub_service")

    if sub:
        lines.append(
            f"🔹 زیرخدمت: {SUB_SERVICE_NAMES.get(sub, sub)}"
        )

    for key, title in FIELD_NAMES.items():

        value = data.get(key)

        if value:
            lines.append(
                f"• {title}: {value}"
            )

    description = data.get("description")

    if description:
        lines.extend(
            [
                "",
                "📝 توضیحات تکمیلی:",
                description,
            ]
        )

    lines.extend(
        [
            "",
            "━━━━━━━━━━━━━━",
            "",
            "در صورت تأیید، درخواست ثبت خواهد شد.",
        ]
    )

    return "\n".join(lines)

# ---------------------------------------------------
# Expert Ticket
# ---------------------------------------------------

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



# ---------------------------------------------------
# Tracking History
# ---------------------------------------------------

def format_user_history(
    request: dict,
    messages: list[dict],
    history: list[dict],
) -> str:

    tracking = request.get(
        "tracking_code",
        "",
    )

    status = STATUS_NAMES.get(
        request.get("status"),
        request.get("status", ""),
    )

    service = SERVICE_NAMES.get(
        request.get("service"),
        request.get("service", ""),
    )

    lines = [
        "📋 وضعیت درخواست",
        "",
        f"🎫 کد پیگیری: {tracking}",
        f"📌 وضعیت: {status}",
        f"🛠 خدمت: {service}",
    ]


    priority = request.get("priority")

    if priority:
        lines.append(
            f"⚡ اولویت: {priority}"
        )


    expert = request.get("expert_name")

    if expert:
        lines.append(
            f"👨‍💼 کارشناس: {expert}"
        )


    created = request.get("created_at")

    if created:
        lines.append(
            f"📅 ثبت: {str(created)}"
        )


    closed = request.get("closed_at")

    if closed:
        lines.append(
            f"✅ خاتمه: {str(closed)}"
        )



    # --------------------------------
    # History
    # --------------------------------

    if history:

        lines.extend(
            [
                "",
                "━━━━━━━━━━━━━━",
                "📜 سوابق",
            ]
        )


        for item in history:

            created = item.get(
                "created_at",
                "",
            )

            event = (
                item.get("description")
                or item.get("event_type")
                or ""
            )


            lines.extend(
                [
                    "",
                    f"• {str(created)}",
                    str(event),
                ]
            )



    # --------------------------------
    # Messages
    # --------------------------------

    if messages:

        lines.extend(
            [
                "",
                "━━━━━━━━━━━━━━",
                "💬 گفتگوها",
            ]
        )


        for msg in messages:

            sender = (
                "👤 شما"
                if msg.get("sender_type") == "USER"
                else "👨‍💼 کارشناس"
            )


            created = msg.get(
                "created_at",
                "",
            )


            lines.extend(
                [
                    "",
                    sender,
                    str(created),
                    str(msg.get("message", "")),
                ]
            )



    return "\n".join(lines)



# ---------------------------------------------------
# Expert Reply
# ---------------------------------------------------

def format_expert_reply(
    tracking: str,
    service: str,
    message: str,
) -> str:

    return "\n".join(
        [
            "📩 پاسخ کارشناس",
            "",
            f"🎫 {tracking}",
            "",
            f"🛠 {SERVICE_NAMES.get(service, service)}",
            "",
            "━━━━━━━━━━━━━━",
            "",
            message,
        ]
    )



# ---------------------------------------------------
# Success
# ---------------------------------------------------

def format_success(
    tracking: str,
) -> str:

    return (
        "✅ درخواست شما با موفقیت ثبت شد.\n\n"
        "کد پیگیری:\n"
        f"{tracking}\n\n"
        "این کد را برای پیگیری نزد خود نگه دارید."
    )
