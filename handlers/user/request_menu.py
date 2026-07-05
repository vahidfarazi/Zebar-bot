"""
handlers/user/request_menu.py

Request menu handler.
"""

from menus import (
    REQUEST_MENU,
    AFTER_SALES_MENU,
)

from form_registry import get_form

from form_engine import FormEngine

from user_state import (
    clear_data,
    set_state,
    update_data,
)


# -----------------------------
# Services
# -----------------------------
AFTER_SALES_SERVICES = {

    "❓ نوع درخواست خود را نمی‌دانم": "UNKNOWN",

    "🔧 اصلاح سرویس": "SERVICE_FIX",

    "🔵 نصب مجدد": "REINSTALL",

    "📍 تغییر مکان": "RELOCATION",

    "👤 تغییر نام": "CHANGE_NAME",

    "⚡ تبدیل آمپراژ": "AMPERAGE",

    "⏸ جمع‌آوری موقت": "TEMP_REMOVE",

    "❌ جمع‌آوری دائم": "PERMANENT_REMOVE",

}


# -----------------------------
# Start Form
# -----------------------------
def start_form(
    chat_id: int,
    service: str,
    sub_service: str | None = None,
):

    clear_data(chat_id)

    update_data(
        chat_id,
        "service",
        service,
    )

    if sub_service:

        update_data(
            chat_id,
            "sub_service",
            sub_service,
        )

    form = get_form(service)

    engine = FormEngine(form)

    first_step = engine.first_step()

    set_state(
        chat_id,
        first_step["state"],
    )

    return {
        "text": f"لطفاً {first_step['title']} را وارد کنید.",
    }


# -----------------------------
# Handle Request Menu
# -----------------------------
def handle_request_menu(
    chat_id: int,
    message: str,
):

    # -----------------------------
    # Register Request
    # -----------------------------
    if message == "📝 ثبت درخواست":

        clear_data(chat_id)

        return {
            "text": "لطفاً خدمت موردنظر را انتخاب کنید.",
            "keyboard": REQUEST_MENU,
        }

    # -----------------------------
    # New Connection
    # -----------------------------
    if message == "🔌 نصب انشعاب جدید":

        return start_form(
            chat_id,
            "NEW_CONNECTION",
        )

    # -----------------------------
    # After Sales Menu
    # -----------------------------
    if message == "🔧 خدمات پس از فروش":

        return {
            "text": "لطفاً نوع خدمت را انتخاب کنید.",
            "keyboard": AFTER_SALES_MENU,
        }

    # -----------------------------
    # After Sales Services
    # -----------------------------
    if message in AFTER_SALES_SERVICES:

        return start_form(
            chat_id,
            "AFTER_SALES",
            AFTER_SALES_SERVICES[message],
        )

    # -----------------------------
    # Meter Test
    # -----------------------------
    if message == "🔍 بازرسی و تست کنتور":

        return start_form(
            chat_id,
            "METER_TEST",
        )

    # -----------------------------
    # Bill Inquiry
    # -----------------------------
    if message == "🧾 بررسی قبض برق":

        return {
            "text": "این بخش در نسخه بعدی فعال خواهد شد.",
        }

    # -----------------------------
    # Back
    # -----------------------------
    if message == "⬅️ بازگشت":

        return {
            "text": "لطفاً خدمت موردنظر را انتخاب کنید.",
            "keyboard": REQUEST_MENU,
        }

    # -----------------------------
    # Main Menu
    # -----------------------------
    if message == "🏠 منوی اصلی":

        return {
            "text": "به منوی اصلی بازگشتید.",
        }

    # -----------------------------
    # Invalid
    # -----------------------------
    return {
        "text": "لطفاً فقط از گزینه‌های موجود استفاده کنید.",
    }
