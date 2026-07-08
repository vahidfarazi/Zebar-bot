"""
callback_handler.py

Handle Bale callback queries.
"""

from bale_client import (
    answer_callback,
    send_message,
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

        if is_waiting_reply(chat_id):

            tracking = get_tracking_code(
                chat_id,
            )

            send_message(

                chat_id=chat_id,

                text=(
                    "⚠️ شما در حال پاسخ به درخواست زیر هستید:\n\n"
                    f"{tracking}\n\n"
                    "ابتدا پاسخ آن را ارسال کنید."
                ),

            )

            return

        tracking = data.split(
            ":",
            1,
        )[1]

        set_waiting_reply(

            chat_id,

            tracking,

        )

        send_message(

            chat_id=chat_id,

            text=(
                "✅ درخواست انتخاب شد.\n\n"
                f"کد رهگیری: {tracking}\n\n"
                "لطفاً پاسخ خود را ارسال کنید."
            ),

        )

        return

    # -----------------------------------------
    # Forward
    # -----------------------------------------
    if data.startswith("forward:"):

        tracking = data.split(
            ":",
            1,
        )[1]

        send_message(

            chat_id=chat_id,

            text=(
                f"ارجاع درخواست {tracking}\n\n"
                "در مرحله بعدی پیاده‌سازی می‌شود."
            ),

        )

        return
