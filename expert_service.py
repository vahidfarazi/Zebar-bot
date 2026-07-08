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
        # Save Message
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
        # Update Group Message
        # -------------------------

        group_chat_id = get_group_chat_id(
            expert_id,
        )

        message_id = get_message_id(
            expert_id,
        )

        if group_chat_id and message_id:

            edit_message(

                chat_id=group_chat_id,

                message_id=message_id,

                text=(
                    "✅ این درخواست پاسخ داده شد.\n\n"
                    f"کد رهگیری: {tracking_code}"
                ),

            )

        # -------------------------
        # Delete Expert Reply
        # -------------------------
        # در نسخه بعدی با داشتن message_id پیام
        # کارشناس از گروه حذف خواهد شد.

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
