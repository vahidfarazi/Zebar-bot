"""
expert_state.py

Expert temporary state manager.
"""

from typing import Optional


# -----------------------------
# Memory Storage
# -----------------------------
_states: dict[int, str] = {}

_data: dict[int, dict] = {}


# -----------------------------
# Set State
# -----------------------------
def set_state(
    chat_id: int,
    state: str,
) -> None:
    """
    Set expert state.
    """

    _states[chat_id] = state


# -----------------------------
# Get State
# -----------------------------
def get_state(
    chat_id: int,
) -> Optional[str]:
    """
    Get expert state.
    """

    return _states.get(chat_id)


# -----------------------------
# Update Data
# -----------------------------
def update_data(
    chat_id: int,
    key: str,
    value,
) -> None:
    """
    Save expert temporary data.
    """

    if chat_id not in _data:

        _data[chat_id] = {}

    _data[chat_id][key] = value


# -----------------------------
# Get Data
# -----------------------------
def get_data(
    chat_id: int,
) -> dict:
    """
    Return expert temporary data.
    """

    return _data.get(
        chat_id,
        {},
    )


# -----------------------------
# Reset
# -----------------------------
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

    _data.pop(
        chat_id,
        None,
    )
