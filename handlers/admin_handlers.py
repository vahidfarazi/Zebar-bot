"""
Admin handlers
"""

from admin_service import get_all_experts
from logger import log_info


def handle_admin_message(chat_id: int, message: str) -> str:
    """
    Handle admin actions.
    """

    log_info("admin_handlers", "message_received", message, user_id=chat_id)

    if message == "کارشناسان":

        experts = get_all_experts()

        return f"تعداد کارشناسان: {len(experts)}"

    return "منوی مدیریت"
