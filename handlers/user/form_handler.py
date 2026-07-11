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


# ------------------------------------
# Handle Form Message
# ------------------------------------
def handle_form(
    chat_id: int,
    message: str,
    state: str,
):

    # --------------------------------
    # Tracking
    # --------------------------------
    if state == "WAITING_TRACKING_CODE":

        result = handle_tracking(
            chat_id,
            message,
        )

        reset(chat_id)

        result["keyboard"] = MAIN_MENU

        return result

    # --------------------------------
    # Cancel
    # --------------------------------
    if message == "❌ انصراف":

        reset(chat_id)

        return {
            "text": "ثبت درخواست لغو شد.",
            "keyboard": MAIN_MENU,
        }

    # --------------------------------
    # Main Menu
    # --------------------------------
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

    # --------------------------------
    # Back
    # --------------------------------
    if message == "⬅️ بازگشت":

        reset(chat_id)

        return {
            "text": "لطفاً خدمت موردنظر را انتخاب کنید.",
            "keyboard": REQUEST_MENU,
        }

    # --------------------------------
    # Load Data
    # --------------------------------
    data = get_data(chat_id)

    service = data.get("service")

    if not service:

        return {
            "text": "ابتدا سرویس را انتخاب کنید.",
            "keyboard": REQUEST_MENU,
        }

    # --------------------------------
    # Load Form
    # --------------------------------
    form = get_form(service)

    if not form:

        return {
            "text": "فرم برای این سرویس تعریف نشده است.",
            "keyboard": REQUEST_MENU,
        }

    engine = FormEngine(form)

    # --------------------------------
    # Current Step
    # --------------------------------
    step = engine.current_step(state)

    # --------------------------------
    # ONE_OF
    # --------------------------------
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

    # --------------------------------
    # Normal Validator
    # --------------------------------
    else:

        if not engine.validate(state, message):

            return {
                "text": (
                    f"❌ مقدار وارد شده برای «{engine.title(state)}» معتبر نیست.\n\n"
                    "لطفاً دوباره وارد کنید."
                ),
                "keyboard": FORM_MENU,
            }

        update_data(
            chat_id,
            engine.field_name(state),
            message,
        )

    # --------------------------------
    # Next Step
    # --------------------------------
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
    # فرم کامل شد
    # مرحله بعد:
    # توضیحات اختیاری
    # =====================================================

    set_state(
        chat_id,
        "WAITING_DESCRIPTION",
    )

    return {
        "text": (
            "📝 **توضیحات تکمیلی (اختیاری)**\n\n"
            "در صورت تمایل، توضیحات تکمیلی یا هر نکته‌ای که "
            "به بررسی سریع‌تر درخواست شما کمک می‌کند را وارد کنید.\n\n"
            "حداکثر ۳۰۰ کاراکتر.\n\n"
            "اگر توضیحی ندارید، گزینه «بدون توضیح» را انتخاب کنید."
        ),
        "keyboard": [
            [
                "📝 ثبت توضیحات",
            ],
            [
                "⏭ بدون توضیح",
            ],
            [
                "❌ انصراف",
            ],
        ],
    }
