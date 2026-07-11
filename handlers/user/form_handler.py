"""
handlers/user/form_handler.py

Generic request form handler (v5).
"""

from menus import (
    MAIN_MENU,
    REQUEST_MENU,
    FORM_MENU,
)

from form_engine import FormEngine
from form_registry import get_form

from validators import detect_identifier

from user_state import (
    get_data,
    update_data,
    set_state,
    reset,
)

from handlers.tracking_handlers import (
    handle_tracking,
)

MAX_DESCRIPTION = 300


def handle_form(
    chat_id: int,
    message: str,
    state: str,
):

    # -------------------------
    # Tracking
    # -------------------------
    if state == "WAITING_TRACKING_CODE":

        result = handle_tracking(
            chat_id,
            message,
        )

        reset(chat_id)

        result["keyboard"] = MAIN_MENU

        return result

    # -------------------------
    # توضیحات تکمیلی
    # -------------------------
    if state == "WAITING_DESCRIPTION":

        from handlers.user.description_handler import (
            handle_description,
        )

        return handle_description(
            chat_id,
            message,
        )

    # -------------------------
    # تأیید نهایی
    # -------------------------
    if state == "WAITING_CONFIRM":

        from handlers.user.description_handler import (
            handle_confirm,
        )

        return handle_confirm(
            chat_id,
            message,
        )

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
                "به سامانه هوشمند خدمات مشترکین "
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
    # Current Step
    # -------------------------
    step = engine.current_step(state)

    # -------------------------
    # ONE_OF validator
    # -------------------------
    if step["validator"] == "ONE_OF":

        identifier_type = detect_identifier(message)

        if identifier_type is None:

            return {
                "text": (
                    "❌ اطلاعات وارد شده معتبر نیست.\n\n"
                    "لطفاً یکی از شناسه‌های مجاز را وارد کنید."
                ),
                "keyboard": FORM_MENU,
            }

        update_data(
            chat_id,
            identifier_type,
            message,
        )

    else:

        if not engine.validate(
            state,
            message,
        ):

            return {
                "text": (
                    f"❌ مقدار وارد شده برای «{engine.title(state)}» نامعتبر است.\n\n"
                    "لطفاً دوباره وارد کنید."
                ),
                "keyboard": FORM_MENU,
            }

        field = engine.field_name(state)

        update_data(
            chat_id,
            field,
            message,
        )

    # -------------------------
    # Reload data
    # -------------------------
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

    # =====================================================
    # فرم کامل شده است
    # ورود به مرحله توضیحات اختیاری
    # =====================================================

    set_state(
        chat_id,
        "WAITING_DESCRIPTION",
    )

    return {

        "text": (
            "📝 توضیحات تکمیلی (اختیاری)\n\n"
            "در صورت تمایل، توضیحات تکمیلی یا هر نکته‌ای که "
            "به بررسی سریع‌تر درخواست شما کمک می‌کند را وارد کنید.\n\n"
            f"حداکثر {MAX_DESCRIPTION} کاراکتر.\n\n"
            "اگر توضیحی ندارید، گزینه «بدون توضیح» را انتخاب کنید."
        ),

        "keyboard": [

            ["⏭ بدون توضیح"],

            ["❌ انصراف"],

        ],

    }
