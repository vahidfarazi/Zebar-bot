"""
handlers/expert_handlers.py

Expert message handler.
"""

from expert_state import (
    get_state,
    get_data,
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

    state = get_state(chat_id)

    # ---------------------------------
    # Waiting Reply
    # ---------------------------------
    if state == "WAITING_REPLY":

        data = get_data(chat_id)

        tracking = data.get("tracking_code")

        if not tracking:

            reset(chat_id)

            return {
                "text": "اطلاعات درخواست یافت نشد.",
            }

        result = reply(

            tracking_code=tracking,

            expert_id=chat_id,

            message=message,

        )

        reset(chat_id)

        if result["success"]:

            return {

                "text":
                    "✅ پاسخ با موفقیت برای مشترک ارسال شد.\n"
                    "درخواست نیز بسته شد.",

            }

        return {

            "text": result["message"],

        }

    # ---------------------------------
    # Default
    # ---------------------------------
    return {

        "text":
            "برای پاسخ به یک درخواست از دکمه «💬 پاسخ» استفاده کنید.",

    }
