"""
state_manager.py

Manages user conversation state safely and consistently.
"""

from database import get_connection
from logger import log_error, log_warning


# -----------------------------
# Get User State
# -----------------------------
def get_user_state(chat_id: int) -> str:
    """
    Retrieve user state from database.
    Default: MAIN_MENU
    """

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT state FROM users WHERE chat_id = ?",
            (chat_id,)
        )

        row = cursor.fetchone()
        conn.close()

        if not row or not row["state"]:
            return "MAIN_MENU"

        return row["state"]

    except Exception as e:
        log_error("state_manager", f"GET_STATE_FAILED: {e}")
        return "MAIN_MENU"


# -----------------------------
# Set User State
# -----------------------------
def set_user_state(chat_id: int, state: str) -> bool:
    """
    Update user state in database.
    Returns success status.
    """

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE users
            SET state = ?
            WHERE chat_id = ?
            """,
            (state, chat_id)
        )

        conn.commit()
        conn.close()

        return True

    except Exception as e:
        log_error("state_manager", f"SET_STATE_FAILED: {e}")
        return False


# -----------------------------
# Reset State
# -----------------------------
def reset_state(chat_id: int) -> bool:
    """
    Reset user state to MAIN_MENU.
    """

    return set_user_state(chat_id, "MAIN_MENU")
