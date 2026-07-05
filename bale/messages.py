"""
bale/messages.py

Send messages to Bale.
"""

import requests

from logger import log_error

from .constants import (
    BASE_URL,
    SEND_MESSAGE,
)

from .keyboards import (
    reply_keyboard,
    inline_keyboard,
)


# -----------------------------
# Send Message
# -----------------------------
def send_message(
    chat_id: int,
    text: str,
    reply_markup=None,
    inline_markup=None,
    parse_mode=None,
):

    payload = {

        "chat_id": chat_id,

        "text": text,

    }

    # -----------------------------
    # Parse Mode
    # -----------------------------
    if parse_mode:

        payload["parse_mode"] = parse_mode

    # -----------------------------
    # Reply Keyboard
    # -----------------------------
    if reply_markup:

        payload["reply_markup"] = reply_keyboard(
            reply_markup,
        )

    # -----------------------------
    # Inline Keyboard
    # -----------------------------
    elif inline_markup:

        payload["reply_markup"] = inline_keyboard(
            inline_markup,
        )

    try:

        response = requests.post(

            BASE_URL + SEND_MESSAGE,

            json=payload,

            timeout=20,

        )

        response.raise_for_status()

        data = response.json()

        if not data.get("ok", False):

            raise Exception(str(data))

        return data

    except Exception as e:

        log_error(

            "bale",

            "send_message",

            str(e),

        )

        return None
