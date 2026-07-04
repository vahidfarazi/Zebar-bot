"""
Tracking handlers
"""

from validators import validate_tracking_code
from database import fetch_one
from logger import log_info


def handle_tracking_message(chat_id: int, message: str):
    """
    Handle tracking code queries.
    """

    if not validate_tracking_code(message):
        return None

    request = fetch_one(
        "SELECT * FROM requests WHERE tracking_code = ?",
        (message,),
    )

    log_info("tracking_handlers", "tracking_search", message, user_id=chat_id)

    if not request:
        return "درخواستی با این شماره رهگیری یافت نشد."

    return (
        f"شماره رهگیری: {request['tracking_code']}\n"
        f"وضعیت: {request['status']}\n"
        f"خدمت: {request['service']}"
    )
