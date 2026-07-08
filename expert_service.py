"""
expert_service.py

Business logic for expert operations.
"""

from typing import Dict, Any

from database import (
    get_request_by_tracking,
    add_message,
    close_request,
)

from notification_service import (
    notify_user,
)

from bale_client import (
    edit_message,
    delete_message,
)

from expert_state import (
    get_group_chat_id,
    get_message_id,
)

from logger import (
    log_info,
    log_error,
)


# -----------------------------
# Reply
# -----------------------------
def reply(
    tracking_code: str,
    expert_id: int,
    message: str,
    reply_message_id: int | None = None,
) -> Dict[str, Any]:
    """
    Save expert reply,
    notify user,
    close request.
    """

    try:

        request = get_request_by_tracking(
            tracking_code,
        )

        if not request:

            return {

                "success": False,

                "message": "درخواست پیدا نشد.",

            }

        # -------------------------
        # Save Reply
        # -------------------------

        add_message(

            tracking_code=tracking_code,

            sender_type="EXPERT",

            sender_id=expert_id,

            message_type="REPLY",

            message=message,

        )

        # -------------------------
        # Notify User
        # -------------------------

        notify_user(

            chat_id=request["chat_id"],

            message=(
                "📩 پاسخ کارشناس\n\n"
                f"{message}"
            ),

        )

        # -------------------------
        # Close Request
        # -------------------------

        close_request(
            request["id"],
        )

        # -------------------------
        # Edit Group Message
        # -------------------------

        group_chat_id = get_group_chat_id(
            expert_id,
        )

        request_message_id = get_message_id(
            expert_id,
        )

        if group_chat_id and request_message_id:

            edit_message(

                chat_id=group_chat_id,

                message_id=request_message_id,

                text=(
                    "✅ این درخواست پاسخ داده شد.\n\n"
                    f"کد رهگیری: {tracking_code}"
                ),

            )

        # -------------------------
        # Delete Expert Reply
        # -------------------------

        if (

            group_chat_id

            and

            reply_message_id

        ):

            delete_message(

                chat_id=group_chat_id,

                message_id=reply_message_id,

            )

        log_info(

            "expert_service",

            "reply",

            tracking_code,

        )

        return {

            "success": True,

        }

    except Exception as e:

        log_error(

            "expert_service",

            "reply",

            str(e),

        )

        return {

            "success": False,

            "message": "خطای داخلی سیستم",

        }


# -----------------------------
# Assign
# -----------------------------
def assign_request(
    tracking_code: str,
    expert_id: int,
) -> Dict[str, Any]:

    return {

        "success": False,

        "message": "ارجاع در نسخه بعدی فعال می‌شود.",

        }
