"""
main_runner.py

Core runtime processor for Azarakhsh system.
"""

import traceback

from config import Config

from router import route_message
from callback_handler import handle_callback

from logger import (
    log_error,
    log_info,
)

from database import (
    create_user,
    is_admin,
)

from bale_client import (
    send_message,
)

from expert_state import (
    is_waiting_reply,
    get_tracking_code,
    reset,
)

from expert_service import (
    reply,
)

from working_hours import (
    can_create_request,
    availability_message,
)

from handlers.expert_handlers import (
    handle_expert_message,
)


# =================================================
# Send Result
# =================================================

def send_result(
    chat_id:int,
    result,
):

    if result is None:

        return


    if isinstance(result,dict):

        send_message(

            chat_id=chat_id,

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

            chat_id=chat_id,

            text=str(result),

        )



# =================================================
# Process Update
# =================================================

def process_update(
    sender_id:int,
    message:str,
    role:str="USER",
    message_id:int|None=None,
):

    try:

        create_user(
            sender_id,
        )


        # -----------------------------------------
        # Expert Reply Flow
        # -----------------------------------------

        if role == "EXPERT":

            if is_waiting_reply(sender_id):

                tracking = get_tracking_code(
                    sender_id,
                )


                result = reply(

                    tracking_code=tracking,

                    expert_id=sender_id,

                    message=message,

                    reply_message_id=message_id,

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



            result = handle_expert_message(

                sender_id,

                message,

            )


            send_result(

                sender_id,

                result,

            )

            return



        # -----------------------------------------
        # User Create Request Availability
        # -----------------------------------------

        if role == "USER":

            if message == "📝 ثبت درخواست":

                if not can_create_request():

                    send_message(

                        chat_id=sender_id,

                        text=availability_message(),

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


        send_result(

            sender_id,

            result,

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

            text="❌ خطایی رخ داد.",

        )



# =================================================
# Update Entry
# =================================================

def handle_update(
    update:dict,
):

    try:


        callback = update.get(
            "callback_query",
        )


        if callback:

            handle_callback(
                callback,
            )

            return



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


        message_id = message.get(
            "message_id",
        )



        chat = message.get(
            "chat",
            {},
        )


        chat_id = chat.get(
            "id",
        )


        chat_type = chat.get(
            "type",
            "private",
        )



        role = "USER"



        expert_group_id = int(

            Config.get_str(

                "EXPERT_GROUP_ID",

                "0",

            )

        )



        if chat_id == expert_group_id:

            role = "EXPERT"


        elif (
            chat_type == "private"
            and is_admin(sender_id)
        ):

            role = "ADMIN"



        process_update(

            sender_id=sender_id,

            message=text,

            role=role,

            message_id=message_id,

        )



    except Exception:


        traceback.print_exc()


        log_error(

            "runner",

            "handle_update",

            traceback.format_exc(),

        )
