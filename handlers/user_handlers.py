"""
user_handlers.py
"""

from database import create_user

from menus import (
    MAIN_MENU,
    REQUEST_MENU,
    AFTER_SALES_MENU,
)

from user_state import (
    get_state,
    set_state,
)

from validators import (
    validate_request_number,
    validate_national_code,
    validate_mobile,
    validate_computer_code,
    validate_bill_id,
)


# -----------------------------
# Handle User
# -----------------------------
def handle_user_message(
    chat_id: int,
    message: str,
):
    """
    User flow.
    """

    create_user(chat_id)

    state = get_state(chat_id)

    # -----------------------------
    # Main Menu
    # -----------------------------
    if message == "/start":

        return {
            "text": "به سامانه آذرخش خوش آمدید.",
            "keyboard": MAIN_MENU,
        }

    if message == "🏠 منوی اصلی":

        return {
            "text": "منوی اصلی",
            "keyboard": MAIN_MENU,
        }

    # -----------------------------
    # Register Request
    # -----------------------------
    if message == "📝 ثبت درخواست":

        return {
            "text": "لطفاً خدمت موردنظر را انتخاب کنید.",
            "keyboard": REQUEST_MENU,
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
    # New Connection
    # -----------------------------
    if message == "🔌 نصب انشعاب جدید":

        set_state(
            chat_id,
            "WAIT_REQUEST_NUMBER_NEW_CONNECTION",
        )

        return {
            "text": (
                "لطفاً شماره تقاضا ۱۱ رقمی را وارد کنید."
            ),
        }

    # -----------------------------
    # Meter Test
    # -----------------------------
    if message == "🔍 بازرسی و تست کنتور":

        set_state(
            chat_id,
            "WAIT_REQUEST_NUMBER_METER_TEST",
        )

        return {
            "text": (
                "لطفاً شماره تقاضا ۱۱ رقمی را وارد کنید."
            ),
        }

    # -----------------------------
    # Bill
    # -----------------------------
    if message == "🧾 بررسی قبض برق":

        set_state(
            chat_id,
            "WAIT_BILL_ID",
        )

        return {
            "text": (
                "لطفاً شناسه قبض را وارد کنید."
            ),
        }

    # -----------------------------
    # Waiting Request Number
    # -----------------------------
    if state == "WAIT_REQUEST_NUMBER_NEW_CONNECTION":

        if not validate_request_number(message):

            return {
                "text": "شماره تقاضا نامعتبر است."
            }

        return {
            "text": "مرحله بعدی..."
        }

    # -----------------------------
    # Default
    # -----------------------------
    return {
        "text": "لطفاً از دکمه‌های موجود استفاده کنید.",
        "keyboard": MAIN_MENU,
    }
