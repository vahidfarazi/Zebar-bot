"""
callback_handler.py

Handle Bale callback queries.
"""

from bale_client import (
    answer_callback,
)

from expert_state import (
    set_waiting_reply,
    is_waiting_reply,
    get_tracking_code,
)


# -------------------------------------------------
# Handle Callback
# -------------------------------------------------
def handle_callback(
    callback: dict,
):

    callback_id = callback.get("id")

    data = callback.get("data", "")

    user = callback.get("from", {})

    expert_id = user.get("id")

    message = callback.get("message", {})

    group_chat = message.get("chat", {})

    group_chat_id = group_chat.get("id")

    message_id = message.get("message_id")

    if callback_id:

        answer_callback(
            callback_id,
        )

    if not expert_id:

        return

    # -----------------------------------------
    # Reply
    # -----------------------------------------
    if data.startswith("reply:"):

        if is_waiting_reply(expert_id):

            return

        tracking = data.split(
            ":",
            1,
        )[1]

        set_waiting_reply(

            chat_id=expert_id,

            tracking_code=tracking,

            group_chat_id=group_chat_id,

            message_id=message_id,

        )

        return

    # -----------------------------------------
    # Forward
    # -----------------------------------------
    if data.startswith("forward:"):

        # مرحله بعدی پیاده‌سازی می‌شود
        return
