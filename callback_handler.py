"""
callback_handler.py

Handle inline keyboard callbacks.
"""

from bale_client import answer_callback

from expert_state import (
    set_state,
    update_data,
)

from logger import (
    log_info,
)


# ---------------------------------
# Handle Callback
# ---------------------------------
def handle_callback(callback: dict):

    callback_id = callback.get("id")

    data = callback.get("data", "")

    message = callback.get("message", {})

    chat = message.get("chat", {})

    chat_id = chat.get("id")

    from_user = callback.get("from", {})

    expert_id = from_user.get("id")

    if callback_id:

        answer_callback(callback_id)

    if not data:

        return

    # ---------------------------------
    # Reply
    # ---------------------------------
    if data.startswith("reply:"):

        tracking = data.split(":", 1)[1]

        set_state(
            expert_id,
            "WAITING_REPLY",
        )

        update_data(
            expert_id,
            "tracking_code",
            tracking,
        )

        from bale_client import send_message

        send_message(

            chat_id=expert_id,

            text=(
                f"🎫 {tracking}\n\n"
                "لطفاً پاسخ خود را برای مشترک ارسال کنید."
            ),

        )

        log_info(
            "callback",
            "reply",
            tracking,
        )

        return

    # ---------------------------------
    # Forward
    # ---------------------------------
    if data.startswith("forward:"):

        tracking = data.split(":", 1)[1]

        from bale_client import send_message

        send_message(

            chat_id=expert_id,

            text=(
                f"ارجاع درخواست\n\n"
                f"{tracking}\n\n"
                "این بخش در نسخه بعدی فعال می‌شود."
            ),

        )

        log_info(
            "callback",
            "forward",
            tracking,
        )

        return
