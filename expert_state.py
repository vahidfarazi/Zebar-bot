"""
expert_state.py

Expert temporary state manager.
"""

from typing import Optional


# -------------------------------------------------
# Memory Storage
# -------------------------------------------------

_states: dict[int, dict] = {}


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
    Expert starts replying to a request.
    """

    _states[chat_id] = {

        "state": "WAITING_REPLY",

        "tracking_code": tracking_code,

        "group_chat_id": group_chat_id,

        "message_id": message_id,

    }


# -------------------------------------------------
# Get State
# -------------------------------------------------
def get_state(
    chat_id: int,
) -> Optional[dict]:
    """
    Return expert state.
    """

    return _states.get(chat_id)


# -------------------------------------------------
# Is Waiting Reply
# -------------------------------------------------
def is_waiting_reply(
    chat_id: int,
) -> bool:
    """
    Check whether expert is waiting for reply.
    """

    state = _states.get(chat_id)

    if not state:

        return False

    return state.get("state") == "WAITING_REPLY"


# -------------------------------------------------
# Get Tracking Code
# -------------------------------------------------
def get_tracking_code(
    chat_id: int,
) -> Optional[str]:
    """
    Return tracking code of current reply.
    """

    state = _states.get(chat_id)

    if not state:

        return None

    return state.get("tracking_code")


# -------------------------------------------------
# Get Group Chat ID
# -------------------------------------------------
def get_group_chat_id(
    chat_id: int,
) -> Optional[int]:
    """
    Return expert group chat id.
    """

    state = _states.get(chat_id)

    if not state:

        return None

    return state.get("group_chat_id")


# -------------------------------------------------
# Get Message ID
# -------------------------------------------------
def get_message_id(
    chat_id: int,
) -> Optional[int]:
    """
    Return request message id inside group.
    """

    state = _states.get(chat_id)

    if not state:

        return None

    return state.get("message_id")


# -------------------------------------------------
# Reset
# -------------------------------------------------
def reset(
    chat_id: int,
) -> None:
    """
    Clear expert state.
    """

    _states.pop(
        chat_id,
        None,
    )
