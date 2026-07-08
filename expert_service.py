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

from logger import (
    log_info,
    log_error,
)


# ---------------------------------
# Reply
# ---------------------------------
def reply(
    tracking_code: str,
    expert_id: int,
    message: str,
) -> Dict[str, Any]:

    try:

        request = get_request_by_tracking(
            tracking_code,
        )

        if not request:

            return {

                "success": False,

                "message": "درخواست پیدا نشد.",

            }

        # -----------------------------
        # Save expert message
        # -----------------------------
        add_message(

            tracking_code=tracking_code,

            sender_type="EXPERT",

            sender_id=expert_id,

            message_type="REPLY",

            message=message,

        )

        # -----------------------------
        # Send to user
        # -----------------------------
        notify_user(

            request["chat_id"],

            (
                "📩 پاسخ کارشناس\n\n"

                f"🎫 {tracking_code}\n\n"

                f"{message}"
            ),

        )

        # -----------------------------
        # Close request
        # -----------------------------
        close_request(
            request["id"],
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

            "message": "خطا در ثبت پاسخ.",

        }


# ---------------------------------
# Assign (Version 2)
# ---------------------------------
def assign_request(
    tracking_code: str,
    expert_id: int,
):

    return {

        "success": False,

        "message": "در نسخه بعدی فعال می‌شود.",

    }
