"""
bale_client.py

Official Bale Bot API client.
"""

import requests

from config import Config
from logger import log_error, log_info


# -----------------------------
# Config
# -----------------------------
BASE_URL = Config.get_str(
    "BALE_API_URL",
    "https://tapi.bale.ai",
)

BOT_TOKEN = Config.get_str(
    "BALE_BOT_TOKEN",
    "",
)


# -----------------------------
# Internal Request
# -----------------------------
def _post(
    method: str,
    payload: dict,
):

    if not BOT_TOKEN:

        log_error(
            "bale_client",
            "missing_token",
            "BALE_BOT_TOKEN is not set",
        )

        return None

    try:

        response = requests.post(

            f"{BASE_URL}/bot{BOT_TOKEN}/{method}",

            json=payload,

            timeout=20,

        )

        if response.status_code != 200:

            log_error(

                "bale_client",

                method,

                response.text,

            )

            return None

        return response.json()

    except Exception as e:

        log_error(

            "bale_client",

            method,

            str(e),

        )

        return None


# -----------------------------
# Send Message
# -----------------------------
def send_message(
    chat_id: int,
    text: str,
    keyboard: list | None = None,
):

    payload = {

        "chat_id": chat_id,

        "text": text,

    }

    if keyboard:

        payload["reply_markup"] = {

            "inline_keyboard": keyboard,

        }

    result = _post(

        "sendMessage",

        payload,

    )

    if result:

        log_info(

            "bale_client",

            "send_message",

            str(chat_id),

        )

    return result


# -----------------------------
# Edit Message
# -----------------------------
def edit_message(

    chat_id: int,

    message_id: int,

    text: str,

    keyboard=None,

):

    payload = {

        "chat_id": chat_id,

        "message_id": message_id,

        "text": text,

    }

    if keyboard:

        payload["reply_markup"] = {

            "inline_keyboard": keyboard,

        }

    return _post(

        "editMessageText",

        payload,

    )


# -----------------------------
# Delete Message
# -----------------------------
def delete_message(

    chat_id: int,

    message_id: int,

):

    payload = {

        "chat_id": chat_id,

        "message_id": message_id,

    }

    return _post(

        "deleteMessage",

        payload,

    )


# -----------------------------
# Answer Callback
# -----------------------------
def answer_callback(

    callback_id: str,

    text: str = "",

):

    payload = {

        "callback_query_id": callback_id,

    }

    if text:

        payload["text"] = text

    return _post(

        "answerCallbackQuery",

        payload,

    )
