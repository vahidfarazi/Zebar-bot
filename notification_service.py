"""
notification_service.py

Notification service.
"""

from config import Config

from bale_client import send_message

from logger import (
    log_info,
    log_error,
)


# ---------------------------------
# Expert Inline Keyboard
# ---------------------------------
def expert_keyboard(
    tracking_code: str,
):

    return [

        [

            ("💬 پاسخ", f"reply:{tracking_code}"),

            ("🔄 ارجاع", f"forward:{tracking_code}"),

        ]

    ]


# ---------------------------------
# Notify Expert Group
# ---------------------------------
def notify_experts(
    tracking_code: str,
    message: str,
) -> bool:

    group_id = Config.get_str(
        "EXPERT_GROUP_ID",
        "",
    )

    if not group_id:

        log_error(
            "notification",
            "expert_group",
            "EXPERT_GROUP_ID is not set",
        )

        return False

    result = send_message(

        chat_id=int(group_id),

        text=message,

        inline_keyboard=expert_keyboard(
            tracking_code,
        ),

    )

    if result:

        log_info(

            "notification",

            "expert_group",

            "sent",

        )

    else:

        log_error(

            "notification",

            "expert_group",

            "failed",

        )

    return result


# ---------------------------------
# Notify User
# ---------------------------------
def notify_user(
    chat_id: int,
    message: str,
    keyboard=None,
) -> bool:

    result = send_message(

        chat_id=chat_id,

        text=message,

        keyboard=keyboard,

    )

    if result:

        log_info(

            "notification",

            "user",

            str(chat_id),

        )

    else:

        log_error(

            "notification",

            "user",

            "failed",

        )

    return result
