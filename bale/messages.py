"""
bale/messages.py

Message operations for Bale Bot API.
"""

from .client import post

from .constants import (
    SEND_MESSAGE,
    EDIT_MESSAGE,
    DELETE_MESSAGE,
    ANSWER_CALLBACK,
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

    if parse_mode:

        payload["parse_mode"] = parse_mode

    if reply_markup:

        payload["reply_markup"] = reply_keyboard(
            reply_markup,
        )

    elif inline_markup:

        payload["reply_markup"] = inline_keyboard(
            inline_markup,
        )

    return post(
        SEND_MESSAGE,
        payload,
    )


# -----------------------------
# Edit Message
# -----------------------------
def edit_message(
    chat_id: int,
    message_id: int,
    text: str,
    inline_markup=None,
):

    payload = {

        "chat_id": chat_id,

        "message_id": message_id,

        "text": text,

    }

    if inline_markup:

        payload["reply_markup"] = inline_keyboard(
            inline_markup,
        )

    return post(
        EDIT_MESSAGE,
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

    return post(
        DELETE_MESSAGE,
        payload,
    )


# -----------------------------
# Answer Callback
# -----------------------------
def answer_callback(
    callback_query_id: str,
    text: str | None = None,
):

    payload = {

        "callback_query_id": callback_query_id,

    }

    if text:

        payload["text"] = text

    return post(
        ANSWER_CALLBACK,
        payload,
    )
