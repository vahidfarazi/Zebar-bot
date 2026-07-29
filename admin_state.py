"""
admin_state.py

Admin temporary state manager.
Used for multi-step admin operations.
"""

from database import (
    get_setting,
    set_setting,
)



# =================================================
# Keys
# =================================================

def _state_key(chat_id: int) -> str:
    return f"ADMIN_STATE_{chat_id}"



def _data_key(chat_id: int) -> str:
    return f"ADMIN_DATA_{chat_id}"



# =================================================
# State
# =================================================

def get_admin_state(
    chat_id: int,
) -> str:

    state = get_setting(
        _state_key(chat_id),
    )

    return state or ""



def set_admin_state(
    chat_id: int,
    state: str,
) -> None:

    set_setting(
        _state_key(chat_id),
        state,
    )



def clear_admin_state(
    chat_id: int,
) -> None:

    set_setting(
        _state_key(chat_id),
        "",
    )



# =================================================
# Temporary Data
# =================================================

def get_admin_data(
    chat_id: int,
) -> dict:

    import json


    value = get_setting(
        _data_key(chat_id),
    )


    if not value:

        return {}



    try:

        return json.loads(
            value,
        )

    except Exception:

        return {}



def save_admin_data(
    chat_id: int,
    data: dict,
) -> None:

    import json


    set_setting(

        _data_key(chat_id),

        json.dumps(
            data,
            ensure_ascii=False,
        ),

    )



def clear_admin_data(
    chat_id: int,
) -> None:

    save_admin_data(
        chat_id,
        {},
    )



# =================================================
# Reset
# =================================================

def reset_admin_session(
    chat_id: int,
) -> None:

    clear_admin_state(
        chat_id,
    )

    clear_admin_data(
        chat_id,
    )
