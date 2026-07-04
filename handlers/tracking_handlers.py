"""
tracking_handlers.py
"""

from request_service import get_request_info
from validators import validate_tracking


# -----------------------------
# Handle Tracking Message
# -----------------------------
def handle_tracking_message(chat_id: int, message: str) -> str:
    """
    Handle tracking code queries.

    Returns response string or empty string if not tracking.
    """

    if not isinstance(message, str):
        return ""

    message = message.strip()

    if not validate_tracking(message):
        return ""

    result = get_request_info(message)

    if not result["success"]:
        return result["message"]

    data = result["data"]

    return (
        f"📦 وضعیت درخواست:\n"
        f"کد: {data['tracking_code']}\n"
        f"وضعیت: {data['status']}\n"
        f"عنوان: {data['title']}"
    )
