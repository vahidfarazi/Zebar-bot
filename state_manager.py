"""
state_manager.py

Manages user conversation states.
Used by router and handlers to determine current flow.
"""

from database import get_connection


# -----------------------------
# Get User State
# -----------------------------
def get_user_state(chat_id: int) -> str:
    """
    Retrieve current conversation state for user.
    Default: MAIN_MENU
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT state FROM users WHERE chat_id = ?",
        (chat_id,)
    )

    row = cursor.fetchone()

    if not row or not row[0]:
        return "MAIN_MENU"

    return row[0]


# -----------------------------
# Set User State
# -----------------------------
def set_user_state(chat_id: int, state: str) -> None:
    """
    Update conversation state for user.
    """

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
