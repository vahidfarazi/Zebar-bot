"""
User handlers - normal user flow
"""

from request_service import create_request
from working_hours import can_create_request
from logger import log_info


def handle_user_message(chat_id: int, message: str) -> str:
    """
    Handle normal user messages.
    """

    log_info("user_handlers", "message_received", message, user_id=chat_id)

    if message == "ثبت درخواست":

        if not can_create_request():
            return "در حال حاضر امکان ثبت درخواست وجود ندارد."

        tracking = create_request(
            chat_id=chat_id,
            service="GENERAL",
            sub_service="OTHER",
        )

        if tracking:
            return f"درخواست شما ثبت شد.\nکد رهگیری:\n{tracking}"

        return "خطا در ثبت درخواست."

    return "پیام شما دریافت شد."
