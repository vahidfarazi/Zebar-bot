"""
handlers/user/request_menu.py

Request menu handler.
"""

from menus import (
    REQUEST_MENU,
    AFTER_SALES_MENU,
    MAIN_MENU,
    FORM_MENU,
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

    if not form:

        print("FORM NOT FOUND:", service)

        return {
            "text": "فرم این خدمت تعریف نشده است.",
            "keyboard": REQUEST_MENU,
        }

    engine = FormEngine(form)

    first_step = engine.first_step()

    set_state(
        chat_id,
        first_step["state"],
    )

    print("FORM STARTED:", service)

    return {
        "text": first_step["title"],
        "keyboard": FORM_MENU,
    }


# -----------------------------
# Handle Request Menu
# -----------------------------
def handle_request_menu(
    chat_id: int,
    message: str,
):

    print("REQUEST MENU MESSAGE:", repr(message))

    # -----------------------------
    # Register Request
    # -----------------------------
    if message == "📝 ثبت درخواست":

        print("REGISTER REQUEST CLICKED")

        clear_data(chat_id)

        return {
            "text": "لطفاً خدمت موردنظر را انتخاب کنید.",
            "keyboard": REQUEST_MENU,
        }

    # -----------------------------
    # New Connection
    # -----------------------------
    if message == "🔌 نصب انشعاب جدید":

        print("NEW CONNECTION")

        return start_form(
            chat_id,
            "NEW_CONNECTION",
        )

    # -----------------------------
    # After Sales
    # -----------------------------
    if message == "🔧 خدمات پس از فروش":

        print("AFTER SALES")

        return {
            "text": "لطفاً نوع خدمت را انتخاب کنید.",
            "keyboard": AFTER_SALES_MENU,
        }

    # -----------------------------
    # After Sales Sub Services
    # -----------------------------
    if message in AFTER_SALES_SERVICES:

        print("AFTER SALES SUB:", message)

        return start_form(
            chat_id,
            "AFTER_SALES",
            AFTER_SALES_SERVICES[message],
        )

    # -----------------------------
    # Meter Test
    # -----------------------------
    if message == "🔍 بازرسی و تست کنتور":

        print("METER TEST")

        return start_form(
            chat_id,
            "METER_TEST",
        )

    # -----------------------------
    # Bill Inquiry
    # -----------------------------
    if message == "🧾 بررسی قبض برق":

        print("BILL INQUIRY")

        return start_form(
            chat_id,
            "BILL_INQUIRY",
        )

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

        clear_data(chat_id)

        return {
            "text": (
                "به سامانه هوشمند خدمات مشترکین "
                "شرکت توزیع نیروی برق استان خراسان رضوی "
                "(آذرخش) خوش آمدید.\n\n"
                "لطفاً خدمت موردنظر را انتخاب کنید."
            ),
            "keyboard": MAIN_MENU,
        }

    # -----------------------------
    # Invalid
    # -----------------------------
    print("INVALID REQUEST MENU")

    return {
        "text": "لطفاً فقط از گزینه‌های موجود استفاده کنید.",
    }
