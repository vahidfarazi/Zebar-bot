"""
handlers/expert_handlers.py

Expert message handler.
"""

from expert_state import (
    is_waiting_reply,
    get_tracking_code,
    reset,
)

from expert_service import (
    reply,
)


# -----------------------------
# Handle Expert Message
# -----------------------------
def handle_expert_message(
    chat_id: int,
    message: str,
):
    """
    Expert workflow.
    """

    # ---------------------------------
    # Waiting Reply
    # ---------------------------------
    if is_waiting_reply(chat_id):

        tracking = get_tracking_code(
            chat_id,
        )

        if not tracking:

            reset(
                chat_id,
            )

            return {

                "text":
                    "اطلاعات درخواست یافت نشد.",

            }

        result = reply(

            tracking_code=tracking,

            expert_id=chat_id,

            message=message,

        )

        reset(
            chat_id,
        )

        if result["success"]:

            return {

                "text":
                    "✅ پاسخ برای مشترک ارسال شد.\n"
                    "درخواست نیز بسته شد.",

            }

        return {

            "text":
                result["message"],

        }

    # ---------------------------------
    # Default
    # ---------------------------------

    return {

        "text":
            "برای پاسخ به درخواست‌ها از دکمه «💬 پاسخ» در گروه کارشناسان استفاده کنید.",

    }
