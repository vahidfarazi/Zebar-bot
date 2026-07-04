"""
expert_handlers.py
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
            return "فرمت: reply request_id message"

        request_id = int(parts[1])
        msg = " ".join(parts[2:])

        result = reply(request_id, chat_id, msg)

        return "ارسال شد" if result["success"] else result["message"]

    # -------------------------
    # Close
    # -------------------------
    if cmd == "close":
        if len(parts) < 2:
            return "فرمت: close request_id"

        result = close(int(parts[1]), chat_id)

        return "بسته شد" if result["success"] else result["message"]

    # -------------------------
    # Assign (optional)
    # -------------------------
    if cmd == "assign":
        if len(parts) < 3:
            return "فرمت: assign request_id expert_id"

        result = assign_request(int(parts[1]), int(parts[2]))

        return "انجام شد" if result["success"] else result["message"]

    return "دستور نامعتبر است"
