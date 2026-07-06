"""
handlers/user/form_handler.py

Generic request form handler (v2).
"""

from form_engine import FormEngine
from form_registry import get_form

from user_state import (
    get_data,
    update_data,
    set_state,
    reset,
)

from request_service import create_request


# -----------------------------
# Handle Form Message
# -----------------------------
def handle_form(
    chat_id: int,
    message: str,
    state: str,
):

    # -------------------------
    # Cancel
    # -------------------------
    if message == "❌ انصراف":

        reset(chat_id)

        return {
            "text": "ثبت درخواست لغو شد.\n\nبرای ادامه از منوی اصلی استفاده کنید.",
        }

    # -------------------------
    # Main Menu
    # -------------------------
    if message == "🏠 منوی اصلی":

        reset(chat_id)

        return {
            "text": "به سامانه خدمات مشترکین برق آذرخش خوش آمدید.",
        }

    # -------------------------
    # Back
    # -------------------------
    if message == "⬅️ بازگشت":

        reset(chat_id)

        return {
            "text": "لطفاً دوباره خدمت موردنظر را انتخاب کنید.",
        }

    # -------------------------
    # Load user data
    # -------------------------
    data = get_data(chat_id)

    service = data.get("service")

    if not service:

        return {
            "text": "ابتدا سرویس را انتخاب کنید.",
        }

    # -------------------------
    # Load form
    # -------------------------
    form = get_form(service)

    if not form:

        return {
            "text": "فرم برای این سرویس تعریف نشده است.",
        }

    engine = FormEngine(form)

    # -------------------------
    # Validate
    # -------------------------
    if not engine.validate(state, message):

        return {
            "text":
                f"❌ مقدار وارد شده برای «{engine.title(state)}» نامعتبر است.\n\n"
                "لطفاً دوباره وارد کنید یا از «❌ انصراف» استفاده کنید.",
        }

    # -------------------------
    # Save field
    # -------------------------
    field = engine.field_name(state)

    update_data(
        chat_id,
        field,
        message,
    )

    data = get_data(chat_id)

    # -------------------------
    # Next Step
    # -------------------------
    next_step = engine.next_step(state)

    if next_step:

        set_state(
            chat_id,
            next_step["state"],
        )

        return {
            "text":
                f"لطفاً {next_step['title']} را وارد کنید.",
        }

    # -------------------------
    # Finish
    # -------------------------
    result = create_request(
        chat_id,
        data,
    )

    reset(chat_id)

    return {
        "text": result["user_message"],
    }
