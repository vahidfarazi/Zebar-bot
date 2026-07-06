"""
notification_service.py

Notification service.
"""

from config import Config

from bale.messages import send_message

from logger import log_info


# -----------------------------
# Notify Expert Group
# -----------------------------
def notify_experts(
    message: str,
    inline_markup=None,
):
    """
    Send message to expert group.

    Returns:
        Bale API response.
    """

    group_id = Config.get_str(
        "EXPERT_GROUP_ID",
        "",
    )

    if not group_id:
        return None

    result = send_message(

        chat_id=int(group_id),

        text=message,

        inline_markup=inline_markup,

    )

    log_info(

        "notification",

        "expert_group",

        "sent",

    )

    return result


# -----------------------------
# Notify User
# -----------------------------
def notify_user(
    chat_id: int,
    message: str,
    reply_markup=None,
):
    """
    Send message to user.

    Returns:
        Bale API response.
    """

    result = send_message(

        chat_id=chat_id,

        text=message,

        reply_markup=reply_markup,

    )

    log_info(

        "notification",

        "user",

        str(chat_id),

    )

    return result
