"""
bale/callbacks.py

Callback Query functions.
"""

from .client import post

from .constants import (
    ANSWER_CALLBACK,
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
