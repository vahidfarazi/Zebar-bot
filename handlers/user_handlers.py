"""
handlers/user_handlers.py

User message handler.
"""

from database import create_user
from request_service import create_request, get_request_info
from working_hours import can_create_request


# -----------------------------
# Handle User Message
# -----------------------------
def handle_user_message(
    chat_id: int,
    message: str,
) -> str:
    """
    Default user flow.
    """

    create_user(chat_id)

    if not message:
        return "پیام نامعتبر است."

    message = message.strip()

    # -----------------------------
    # Greeting
    # -----------------------------
    greetings = {
        "سلام",
        "سلام.",
        "سلام!",
        "درود",
        "hi",
        "hello",
    }

    if message.lower() in greetings:
        return (
            "🌹 به سامانه آذرخش خوش آمدید.\n\n"
            "لطفاً یکی از گزینه‌های زیر را انتخاب کنید:\n\n"
            "1️⃣ ثبت درخواست\n"
            "2️⃣ پیگیری درخواست\n"
            "3️⃣ راهنما"
        )

    # -----------------------------
    # Help
    # -----------------------------
    if message == "راهنما":
        return (
            "برای ثبت درخواست، عبارت «ثبت درخواست» را ارسال کنید.\n\n"
            "برای پیگیری، کد رهگیری مانند:\n"
            "SR-2026-0000001\n"
            "را ارسال کنید."
        )

    # -----------------------------
    # Tracking
    # -----------------------------
    if message.startswith("SR-"):

        result = get_request_info(message)

        if not result["success"]:
            return result["message"]

        return str(result["data"])

    # -----------------------------
    # Create Request
    # -----------------------------
    if message == "ثبت درخواست":

        if not can_create_request():
            return "در حال حاضر امکان ثبت درخواست وجود ندارد."

        return "لطفاً متن درخواست خود را ارسال کنید."

    # -----------------------------
    # Ignore menu options
    # -----------------------------
    if message in (
        "1",
        "1️⃣",
        "2",
        "2️⃣",
        "3",
        "3️⃣",
        "پیگیری درخواست",
    ):
        return "این بخش در حال تکمیل است."

    # -----------------------------
    # Default: create request
    # -----------------------------
    if not can_create_request():
        return "در حال حاضر امکان ثبت درخواست وجود ندارد."

    result = create_request(
        chat_id,
        "درخواست کاربر",
        message,
    )

    if not result["success"]:
        return result["message"]

    return (
        "✅ درخواست شما ثبت شد.\n\n"
        f"کد پیگیری:\n{result['tracking_code']}"
    )
