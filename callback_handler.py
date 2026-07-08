"""
callback_handler.py

Handle Bale callback queries.
"""

from bale_client import (
    answer_callback,
    edit_message,
)

from expert_state import (
    set_waiting_reply,
    is_waiting_reply,
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

    if callback_id:

        answer_callback(
            callback_id,
        )

    if not expert_id:

        return

    group_chat = message.get(
        "chat",
        {},
    )

    group_chat_id = group_chat.get(
        "id",
    )

    message_id = message.get(
        "message_id",
    )

    text = message.get(
        "text",
        "",
    )

    # -----------------------------------------
    # Reply
    # -----------------------------------------

    if data.startswith("reply:"):

        if is_waiting_reply(
            expert_id,
        ):
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

        try:

            new_text = (
                text
                + "\n\n━━━━━━━━━━━━━━\n"
                + f"✍️ در حال پاسخ توسط کارشناس {expert_id}"
            )

            edit_message(

                chat_id=group_chat_id,

                message_id=message_id,

                text=new_text,

            )

        except Exception:

            pass

        return

    # -----------------------------------------
    # Forward
    # -----------------------------------------

    if data.startswith("forward:"):

        return
