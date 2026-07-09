"""
user_state.py

User state manager.
"""

import json

from database import (
    get_setting,
    set_setting,
)


# -----------------------------
# Keys
# -----------------------------
def _state_key(chat_id: int) -> str:
    return f"STATE_{chat_id}"


def _data_key(chat_id: int) -> str:
    return f"DATA_{chat_id}"


# -----------------------------
# State
# -----------------------------
def get_state(
    chat_id: int,
) -> str:

    state = get_setting(
        _state_key(chat_id),
    )

    return state or ""


def set_state(
    chat_id: int,
    state: str,
) -> None:

    set_setting(
        _state_key(chat_id),
        state,
    )


def clear_state(
    chat_id: int,
) -> None:

    set_setting(
        _state_key(chat_id),
        "",
    )


# -----------------------------
# Form Data
# -----------------------------
def get_data(
    chat_id: int,
) -> dict:

    value = get_setting(
        _data_key(chat_id),
    )

    if not value:

        return {}

    try:

        return json.loads(value)

    except Exception:

        return {}


def save_data(
    chat_id: int,
    data: dict,
) -> None:

    set_setting(

        _data_key(chat_id),

        json.dumps(
            data,
            ensure_ascii=False,
        ),

    )


def update_data(
    chat_id: int,
    key: str,
    value,
) -> None:

    data = get_data(chat_id)

    data[key] = value

    save_data(
        chat_id,
        data,
    )


def clear_data(
    chat_id: int,
) -> None:

    save_data(
        chat_id,
        {},
    )


# -----------------------------
# Reset Session
# -----------------------------
def reset(
    chat_id: int,
) -> None:

    clear_state(chat_id)

    clear_data(chat_id)
