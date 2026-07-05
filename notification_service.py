"""
notification_service.py

Notification service.
"""

from config import Config

from bale_client import send_message

from logger import log_info


# -----------------------------
# Expert Group
# -----------------------------
def notify_experts(
    message: str,
):

    group_id = Config.get_str(
        "EXPERT_GROUP_ID",
        "",
    )

    if not group_id:
        return

    send_message(
        int(group_id),
        message,
    )

    log_info(
        "notification",
        "expert_group",
        "sent",
    )


# -----------------------------
# User
# -----------------------------
def notify_user(
    chat_id: int,
    message: str,
):

    send_message(
        chat_id,
        message,
    )

    log_info(
        "notification",
        "user",
        str(chat_id),
    )
