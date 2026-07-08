"""
bale_client.py

Official Bale Bot API client.
Supports:
- Send Message
- Reply Keyboard
- Inline Keyboard
- Edit Message
- Delete Message
- Answer Callback
"""

import requests

from config import Config
from logger import log_error, log_info


# -------------------------------------------------
# Config
# -------------------------------------------------

BASE_URL = Config.get_str(
    "BALE_API_URL",
    "https://tapi.bale.ai",
)

BOT_TOKEN = Config.get_str(
    "BALE_BOT_TOKEN",
    "",
)


def _url(method: str) -> str:

    return f"{BASE_URL}/bot{BOT_TOKEN}/{method}"


# -------------------------------------------------
# Send Message
# -------------------------------------------------

def send_message(
    chat_id: int,
    text: str,
    keyboard=None,
    inline_keyboard=None,
) -> bool:

    if not BOT_TOKEN:

        log_error(
            "bale_client",
            "missing_token",
            "BALE_BOT_TOKEN is not set",
        )

        return False

    payload = {

        "chat_id": chat_id,

        "text": text,

    }

    # Reply Keyboard
    if keyboard:

        payload["reply_markup"] = {

            "keyboard": keyboard,

            "resize_keyboard": True,

            "one_time_keyboard": False,

        }

    # Inline Keyboard
    elif inline_keyboard:

        payload["reply_markup"] = {

            "inline_keyboard": inline_keyboard,

        }

    try:

        response = requests.post(

            _url("sendMessage"),

            json=payload,

            timeout=20,

        )

        if response.status_code != 200:

            log_error(

                "bale_client",

                "send_failed",

                response.text,

            )

            return False

        log_info(

            "bale_client",

            "send_message",

            str(chat_id),

        )

        return True

    except Exception as e:

        log_error(

            "bale_client",

            "exception",

            str(e),

        )

        return False


# -------------------------------------------------
# Edit Message
# -------------------------------------------------

def edit_message(

    chat_id: int,

    message_id: int,

    text: str,

    inline_keyboard=None,

):

    payload = {

        "chat_id": chat_id,

        "message_id": message_id,

        "text": text,

    }

    if inline_keyboard:

        payload["reply_markup"] = {

            "inline_keyboard": inline_keyboard,

        }

    try:

        requests.post(

            _url("editMessageText"),

            json=payload,

            timeout=20,

        )

        return True

    except Exception as e:

        log_error(

            "bale_client",

            "edit",

            str(e),

        )

        return False


# -------------------------------------------------
# Delete Message
# -------------------------------------------------

def delete_message(

    chat_id: int,

    message_id: int,

):

    try:

        requests.post(

            _url("deleteMessage"),

            json={

                "chat_id": chat_id,

                "message_id": message_id,

            },

            timeout=20,

        )

        return True

    except Exception as e:

        log_error(

            "bale_client",

            "delete",

            str(e),

        )

        return False


# -------------------------------------------------
# Answer Callback
# -------------------------------------------------

def answer_callback(

    callback_query_id: str,

    text: str | None = None,

):

    payload = {

        "callback_query_id": callback_query_id,

    }

    if text:

        payload["text"] = text

    try:

        requests.post(

            _url("answerCallbackQuery"),

            json=payload,

            timeout=20,

        )

        return True

    except Exception as e:

        log_error(

            "bale_client",

            "callback",

            str(e),

        )

        return False
