"""
handlers/user/request_menu.py

Request menus.
"""

from menus import (
    REQUEST_MENU,
    AFTER_SALES_MENU,
)

from forms import (
    NEW_CONNECTION_FORM,
    AFTER_SALES_FORM,
    METER_TEST_FORM,
)

from form_engine import FormEngine

from user_state import (
    clear_data,
    set_state,
    update_data,
)


# -----------------------------
# Request Menu
# -----------------------------
def handle_request_menu(
    chat_id: int,
    message: str,
):

    # -----------------------------
    # Main Request Menu
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

        clear_data(chat_id)

        update_data(
            chat_id,
            "service",
            "NEW_CONNECTION",
        )

        engine = FormEngine(
            NEW_CONNECTION_FORM,
        )

        first = engine.first_step()

        set_state(
            chat_id,
            first["state"],
        )

        return {
            "text": f"لطفاً {first['title']} را وارد کنید.",
        }

    # -----------------------------
    # After Sales
    # -----------------------------
    if message == "🔧 خدمات پس از فروش":

        return {
            "text": "لطفاً نوع خدمت را انتخاب کنید.",
            "keyboard": AFTER_SALES_MENU,
        }

    # -----------------------------
    # After Sales Services
    # -----------------------------
    after_sales_services = {

        "❓ نوع درخواست خود را نمی‌دانم":
            "UNKNOWN",

        "🔧 اصلاح سرویس":
            "SERVICE_FIX",

        "🔵 نصب مجدد":
            "REINSTALL",

        "📍 تغییر مکان":
            "RELOCATION",

        "👤 تغییر نام":
            "CHANGE_NAME",

        "⚡ تبدیل آمپراژ":
            "AMPERAGE",

        "⏸ جمع‌آوری موقت":
            "TEMP_REMOVE",

        "❌ جمع‌آوری دائم":
            "PERMANENT_REMOVE",

    }

    if message in after_sales_services:

        clear_data(chat_id)

        update_data(
            chat_id,
            "service",
            "AFTER_SALES",
        )

        update_data(
            chat_id,
            "sub_service",
            after_sales_services[message],
        )

        engine = FormEngine(
            AFTER_SALES_FORM,
        )

        first = engine.first_step()

        set_state(
            chat_id,
            first["state"],
        )

        return {
            "text": f"لطفاً {first['title']} را وارد کنید.",
        }

    # -----------------------------
    # Meter Test
    # -----------------------------
    if message == "🔍 بازرسی و تست کنتور":

        clear_data(chat_id)

        update_data(
            chat_id,
            "service",
            "METER_TEST",
        )

        engine = FormEngine(
            METER_TEST_FORM,
        )

        first = engine.first_step()

        set_state(
            chat_id,
            first["state"],
        )

        return {
            "text": f"لطفاً {first['title']} را وارد کنید.",
        }

    # -----------------------------
    # Bill Inquiry
    # -----------------------------
    if message == "🧾 بررسی قبض برق":

        return {
            "text":
                "این خدمت در نسخه بعدی فعال خواهد شد.",
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
    # Invalid
    # -----------------------------
    return {
        "text": "لطفاً یکی از گزینه‌های موجود را انتخاب کنید.",
    }
