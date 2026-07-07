"""
handlers/user/form_handler.py

Generic request form handler (v3).
"""

from menus import (
    MAIN_MENU,
    REQUEST_MENU,
    FORM_MENU,
)

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
            "text": "ثبت درخواست لغو شد.",
            "keyboard": MAIN_MENU,
        }

    # -------------------------
    # Main Menu
    # -------------------------
    if message == "🏠 منوی اصلی":

        reset(chat_id)

        return {
            "text": (
                "به سامانه خدمات مشترکین "
                "شرکت توزیع نیروی برق استان خراسان رضوی "
                "(آذرخش) خوش آمدید.\n\n"
                "لطفاً یکی از گزینه‌های زیر را انتخاب کنید."
            ),
            "keyboard": MAIN_MENU,
        }

    # -------------------------
    # Back
    # -------------------------
    if message == "⬅️ بازگشت":

        reset(chat_id)

        return {
            "text": "لطفاً خدمت موردنظر را انتخاب کنید.",
            "keyboard": REQUEST_MENU,
        }

    # -------------------------
    # Load user data
    # -------------------------
    data = get_data(chat_id)

    service = data.get("service")

    if not service:

        return {
            "text": "ابتدا سرویس را انتخاب کنید.",
            "keyboard": REQUEST_MENU,
        }

    # -------------------------
    # Load form
    # -------------------------
    form = get_form(service)

    if not form:

        return {
            "text": "فرم برای این سرویس تعریف نشده است.",
            "keyboard": REQUEST_MENU,
        }

    engine = FormEngine(form)

    # -------------------------
    # Validate
    # -------------------------
    if not engine.validate(state, message):

        return {
            "text":
                f"❌ مقدار وارد شده برای «{engine.title(state)}» نامعتبر است.\n\n"
                "لطفاً دوباره وارد کنید یا از دکمه‌های زیر استفاده کنید.",
            "keyboard": FORM_MENU,
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
            "text": f"لطفاً {next_step['title']} را وارد کنید.",
            "keyboard": FORM_MENU,
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
        "keyboard": MAIN_MENU,
    }
