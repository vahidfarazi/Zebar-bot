"""
expert_handlers.py

Expert command handler (v1).
"""

from expert_service import (
    reply,
    close,
    assign_request,
)


# -----------------------------
# Handle Expert Message
# -----------------------------
def handle_expert_message(chat_id: int, message: str) -> str:
    """
    Expert command handler (MVP keyword-based).
    """

    if not message:
        return "پیام نامعتبر است"

    parts = message.split()
    cmd = parts[0].lower()

    # -------------------------
    # Reply
    # -------------------------
    if cmd == "reply":

        if len(parts) < 3:
            return "فرمت: reply tracking_code message"

        tracking_code = parts[1]
        msg = " ".join(parts[2:])

        result = reply(
            tracking_code,
            chat_id,
            msg,
        )

        return "ارسال شد" if result["success"] else result["message"]

    # -------------------------
    # Close
    # -------------------------
    if cmd == "close":

        if len(parts) < 2:
            return "فرمت: close tracking_code"

        tracking_code = parts[1]

        result = close(
            tracking_code,
            chat_id,
        )

        return "بسته شد" if result["success"] else result["message"]

    # -------------------------
    # Assign
    # -------------------------
    if cmd == "assign":

        if len(parts) < 3:
            return "فرمت: assign tracking_code expert_id"

        tracking_code = parts[1]
        expert_id = int(parts[2])

        result = assign_request(
            tracking_code,
            expert_id,
        )

        return "انجام شد" if result["success"] else result["message"]

    return "دستور نامعتبر است"
