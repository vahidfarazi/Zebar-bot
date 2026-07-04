"""
expert_handlers.py

Handles expert interactions:
- view requests
- reply to requests
- close requests
"""

from expert_service import reply, close
from database import get_request_by_tracking
from logger import log_info
from messages import GENERAL_ERROR, REQUEST_NOT_FOUND


# -----------------------------
# Handle Expert Message
# -----------------------------
def handle_expert_message(chat_id: int, message: str) -> str:
    """
    Process expert commands and messages.
    """

    try:
        message = message.strip()

        # -------------------------
        # Close Request Command
        # /close SR-2026-0000001
        # -------------------------
        if message.startswith("/close"):
            tracking = message.replace("/close", "").strip()

            request = get_request_by_tracking(tracking)

            if not request:
                return REQUEST_NOT_FOUND

            result = close(request["id"], chat_id)

            if result["success"]:
                log_info("expert_handlers", "close", f"expert={chat_id}, req={tracking}")
                return "درخواست با موفقیت بسته شد."

            return GENERAL_ERROR

        # -------------------------
        # Reply to Request
        # /reply SR-2026-0000001|message text
        # -------------------------
        if message.startswith("/reply"):
            content = message.replace("/reply", "").strip().split("|")

            if len(content) < 2:
                return "فرمت پیام اشتباه است."

            tracking = content[0].strip()
            text = content[1].strip()

            request = get_request_by_tracking(tracking)

            if not request:
                return REQUEST_NOT_FOUND

            result = reply(
                request_id=request["id"],
                expert_id=chat_id,
                message=text,
            )

            if result["success"]:
                log_info("expert_handlers", "reply", f"expert={chat_id}")
                return "پاسخ شما ثبت شد."

            return GENERAL_ERROR

        # -------------------------
        # Default fallback
        # -------------------------
        return "دستور نامعتبر است."

    except Exception as e:
        log_info("expert_handlers", "error", str(e))
        return GENERAL_ERROR
