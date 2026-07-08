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

    group = message.get(
        "chat",
        {},
    )

    group_chat_id = group.get(
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

        # کارشناس قبلاً در حال پاسخ است
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

        # ---------------------------------
        # Mark message
        # ---------------------------------

        try:

            new_text = (
                text
                + "\n\n"
                + "━━━━━━━━━━━━━━\n"
                + f"✍️ در حال پاسخ توسط کارشناس {expert_id}"
            )

            edit_message(

                chat_id=group_chat_id,

                message_id=message_id,

                text=new_text,

            )

        except Exception:

            # اگر ویرایش پیام انجام نشد،
            # روند پاسخ متوقف نشود.
            pass

        return

    # -----------------------------------------
    # Forward
    # -----------------------------------------
    if data.startswith("forward:"):

        # مرحله بعد
        return
