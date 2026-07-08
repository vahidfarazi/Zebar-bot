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
) -> None:
    """
    Expert starts replying to a request.
    """

    _states[chat_id] = {

        "state": "WAITING_REPLY",

        "tracking_code": tracking_code,

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
