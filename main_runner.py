"""
main_runner.py

Core runtime processor for Azarakhsh system.
"""

import traceback

from router import route_message
from callback_handler import handle_callback

from logger import (
    log_error,
    log_info,
)

from database import (
    create_user,
    get_expert,
    is_admin,
)

from bale_client import send_message

from expert_state import (
    is_waiting_reply,
    get_tracking_code,
    reset,
)

from expert_service import (
    reply,
)


# -------------------------------------------------
# Process Update
# -------------------------------------------------
def process_update(
    sender_id: int,
    message: str,
    role: str = "USER",
) -> None:
    """
    Process incoming message.
    """

    try:

        create_user(sender_id)

        # -----------------------------------------
        # Expert Waiting Reply
        # -----------------------------------------
        if role == "EXPERT" and is_waiting_reply(sender_id):

            tracking = get_tracking_code(
                sender_id,
            )

            result = reply(

                tracking_code=tracking,

                expert_id=sender_id,

                message=message,

            )

            reset(
                sender_id,
            )

            if not result["success"]:

                send_message(

                    chat_id=sender_id,

                    text=result["message"],

                )

            return

        # -----------------------------------------
        # Router
        # -----------------------------------------

        result = route_message(

            sender_id,

            message,

            role,

        )

        if result is None:

            return

        if isinstance(result, dict):

            send_message(

                chat_id=sender_id,

                text=result.get(
                    "text",
                    "",
                ),

                keyboard=result.get(
                    "keyboard",
                ),

            )

        else:

            send_message(

                chat_id=sender_id,

                text=str(result),

            )

        log_info(

            "runner",

            "process_update",

            str(sender_id),

        )

    except Exception:

        traceback.print_exc()

        log_error(

            "runner",

            "process_update",

            traceback.format_exc(),

        )

        send_message(

            chat_id=sender_id,

            text="خطایی رخ داد.",

        )


# -------------------------------------------------
# Handle Incoming Update
# -------------------------------------------------
def handle_update(
    update: dict,
) -> None:
    """
    Entry point.
    """

    try:

        print("========== UPDATE ==========")
        print(update)
        print("============================")

        # -----------------------------------------
        # Callback
        # -----------------------------------------
        callback = update.get(
            "callback_query",
        )

        if callback:

            handle_callback(
                callback,
            )

            return

        # -----------------------------------------
        # Message
        # -----------------------------------------
        message = update.get(
            "message",
            {},
        )

        if not message:

            return

        sender = message.get(
            "from",
            {},
        )

        sender_id = sender.get(
            "id",
        )

        if not sender_id:

            return

        text = message.get(
            "text",
            "",
        )

        # -----------------------------------------
        # Detect Role
        # -----------------------------------------

        role = "USER"

        if is_admin(sender_id):

            role = "ADMIN"

        elif get_expert(sender_id):

            role = "EXPERT"

        process_update(

            sender_id,

            text,

            role,

        )

    except Exception:

        traceback.print_exc()

        log_error(

            "runner",

            "handle_update",

            traceback.format_exc(),

        )
