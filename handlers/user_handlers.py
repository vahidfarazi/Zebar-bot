"""
user_handlers.py
"""

from database import create_user
from request_service import create_request, get_request_info
from working_hours import can_create_request


# -----------------------------
# Handle User Message
# -----------------------------
def handle_user_message(chat_id: int, message: str) -> str:
    """
    Default user flow.
    """

    create_user(chat_id)

    if not message:
        return "پیام نامعتبر است"

    # Tracking request
    if message.startswith("SR-"):
        result = get_request_info(message)

        if not result["success"]:
            return result["message"]

        return str(result["data"])

    # Create request
    if not can_create_request():
        return "در حال حاضر امکان ثبت درخواست وجود ندارد"

    result = create_request(
        chat_id,
        "درخواست کاربر",
        message,
    )

    if not result["success"]:
        return result["message"]

    return f"درخواست ثبت شد\nکد پیگیری: {result['tracking_code']}"
