"""
expert_state.py

Persistent expert state manager.
"""

import json

from database import (
    get_setting,
    set_setting,
)


# -------------------------------------------------
# Keys
# -------------------------------------------------
def _state_key(
    chat_id: int,
) -> str:

    return f"EXPERT_STATE_{chat_id}"


# -------------------------------------------------
# Save State
# -------------------------------------------------
def _save_state(
    chat_id: int,
    state: dict,
) -> None:

    set_setting(

        _state_key(chat_id),

        json.dumps(
            state,
            ensure_ascii=False,
        ),

    )


# -------------------------------------------------
# Load State
# -------------------------------------------------
def _load_state(
    chat_id: int,
) -> dict:

    value = get_setting(

        _state_key(chat_id),

    )

    if not value:

        return {}

    try:

        return json.loads(value)

    except Exception:

        return {}


# -------------------------------------------------
# Set Waiting Reply
# -------------------------------------------------
def set_waiting_reply(
    chat_id: int,
    tracking_code: str,
    group_chat_id: int,
    message_id: int,
) -> None:
    """
    Expert starts replying.
    """

    _save_state(

        chat_id,

        {

            "state": "WAITING_REPLY",

            "tracking_code": tracking_code,

            "group_chat_id": group_chat_id,

            "message_id": message_id,

        },

    )


# -------------------------------------------------
# Get State
# -------------------------------------------------
def get_state(
    chat_id: int,
) -> dict:

    return _load_state(
        chat_id,
    )


# -------------------------------------------------
# Waiting Reply
# -------------------------------------------------
def is_waiting_reply(
    chat_id: int,
) -> bool:

    state = _load_state(
        chat_id,
    )

    return state.get("state") == "WAITING_REPLY"


# -------------------------------------------------
# Tracking
# -------------------------------------------------
def get_tracking_code(
    chat_id: int,
):

    state = _load_state(
        chat_id,
    )

    return state.get(
        "tracking_code",
    )


# -------------------------------------------------
# Group Chat
# -------------------------------------------------
def get_group_chat_id(
    chat_id: int,
):

    state = _load_state(
        chat_id,
    )

    return state.get(
        "group_chat_id",
    )


# -------------------------------------------------
# Group Message
# -------------------------------------------------
def get_group_message_id(
    chat_id: int,
):

    state = _load_state(
        chat_id,
    )

    return state.get(
        "message_id",
    )


# -------------------------------------------------
# Reset
# -------------------------------------------------
def reset(
    chat_id: int,
) -> None:

    set_setting(

        _state_key(chat_id),

        "",

    )
