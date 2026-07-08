"""
handlers/expert_handlers.py

Expert message handler.
"""


# -------------------------------------------------
# Handle Expert Message
# -------------------------------------------------
def handle_expert_message(
    chat_id: int,
    message: str,
):
    """
    Expert messages.

    پاسخ کارشناس در main_runner.py
    مدیریت می‌شود.

    این فایل فقط پیام‌های عادی کارشناس را مدیریت می‌کند.
    """

    return {

        "text":
            "برای پاسخ به درخواست، از دکمه «💬 پاسخ» در گروه کارشناسان استفاده کنید.",

    }
