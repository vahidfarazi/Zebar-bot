"""
callback_handler.py

Handle Bale callback queries.
"""

from bale_client import answer_callback

from expert_state import (
    set_state,
    update_data,
)

from bale_client import send_message


# -------------------------------------------------
# Handle Callback
# -------------------------------------------------
def handle_callback(
    callback: dict,
):

    callback_id = callback.get("id")

    data = callback.get("data", "")

    user = callback.get("from", {})

    chat_id = user.get("id")

    if callback_id:

        answer_callback(
            callback_id,
        )

    if not chat_id:

        return

    # -----------------------------------------
    # Reply
    # -----------------------------------------
    if data.startswith("reply:"):

        tracking = data.split(":", 1)[1]

        set_state(
            chat_id,
            "WAITING_REPLY",
        )

        update_data(
            chat_id,
            "tracking_code",
            tracking,
        )

        send_message(

            chat_id=chat_id,

            text=(
                "لطفاً پاسخ خود را برای مشترک ارسال کنید."
            ),

        )

        return

    # -----------------------------------------
    # Forward
    # -----------------------------------------
    if data.startswith("forward:"):

        tracking = data.split(":", 1)[1]

        send_message(

            chat_id=chat_id,

            text=(
                f"ارجاع درخواست {tracking} "
                "در نسخه بعدی فعال می‌شود."
            ),

        )

        return
