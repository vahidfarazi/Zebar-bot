"""
Expert handlers
"""

from expert_service import get_expert_requests, reply_to_request
from logger import log_info


def handle_expert_message(chat_id: int, message: str) -> str:
    """
    Handle expert actions.
    """

    log_info("expert_handlers", "message_received", message, user_id=chat_id)

    if message == "درخواست‌های من":
        req = get_expert_requests(chat_id)

        if not req:
            return "درخواستی برای شما وجود ندارد."

        return f"تعداد درخواست‌ها: 1"

    return "منوی کارشناس"
