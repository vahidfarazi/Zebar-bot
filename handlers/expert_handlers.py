"""
handlers/expert_handlers.py

Expert panel handler.
"""

from database import (
    get_expert,
    get_expert_requests,
    get_request,
    close_request,
    update_request_status,
    get_request_by_tracking,
    add_message,
    add_history,
)

from menus import (
    EXPERT_MENU,
    MAIN_MENU,
)

from ticket_formatter import (
    format_request,
)


# ----------------------------------
# Main Handler
# ----------------------------------

def handle_expert_message(
    chat_id: int,
    message: str,
):

    expert = get_expert(chat_id)

    if not expert:

        return {

            "text":
                "⛔ شما به عنوان کارشناس ثبت نشده‌اید.",

            "keyboard":
                MAIN_MENU,

        }

    if message == "/expert":

        return {

            "text":
                "👨‍💼 پنل کارشناس",

            "keyboard":
                EXPERT_MENU,

        }

    parts = message.split()

    cmd = parts[0].lower()

    # ----------------------------------
    # My Requests
    # ----------------------------------

    if cmd == "my_requests":

        requests = get_expert_requests(chat_id)

        if not requests:

            return {

                "text":
                    "درخواستی به شما تخصیص داده نشده است.",

                "keyboard":
                    EXPERT_MENU,

            }

        text = "📋 درخواست‌های من\n\n"

        for item in requests:

            text += (

                f"🎫 {item['tracking_code']}\n"

                f"{item['status']}\n\n"

            )

        return {

            "text": text,

            "keyboard":
                EXPERT_MENU,

        }

    # ----------------------------------
    # View Request
    # ----------------------------------

    if cmd == "view":

        if len(parts) < 2:

            return {

                "text":
                    "فرمت:\nview TRACKING",

                "keyboard":
                    EXPERT_MENU,

            }

        request = get_request_by_tracking(parts[1])

        if not request:

            return {

                "text":
                    "درخواست پیدا نشد.",

                "keyboard":
                    EXPERT_MENU,

            }

        return {

            "text":
                format_request(request),

            "keyboard":
                EXPERT_MENU,

        }

    # ----------------------------------
    # Change Status
    # ----------------------------------

    if cmd == "status":

        if len(parts) < 3:

            return {

                "text":
                    "فرمت:\nstatus TRACKING STATUS",

                "keyboard":
                    EXPERT_MENU,

            }

        request = get_request_by_tracking(parts[1])

        if not request:

            return {

                "text":
                    "درخواست پیدا نشد.",

                "keyboard":
                    EXPERT_MENU,

            }

        update_request_status(

            request["id"],

            parts[2],

        )

        add_history(

            request["tracking_code"],

            "STATUS_CHANGE",

            "EXPERT",

            chat_id,

            f"تغییر وضعیت به {parts[2]}",

        )

        return {

            "text":
                "✅ وضعیت بروزرسانی شد.",

            "keyboard":
                EXPERT_MENU,

        }

    # ----------------------------------
    # Close
    # ----------------------------------

    if cmd == "close":

        if len(parts) < 2:

            return {

                "text":
                    "فرمت:\nclose TRACKING",

                "keyboard":
                    EXPERT_MENU,

            }

        request = get_request_by_tracking(parts[1])

        if not request:

            return {

                "text":
                    "درخواست پیدا نشد.",

                "keyboard":
                    EXPERT_MENU,

            }

        close_request(

            request["id"],

        )

        add_history(

            request["tracking_code"],

            "REQUEST_CLOSED",

            "EXPERT",

            chat_id,

            "درخواست بسته شد.",

        )

        return {

            "text":
                "✅ درخواست بسته شد.",

            "keyboard":
                EXPERT_MENU,

        }

    # ----------------------------------
    # Reply
    # ----------------------------------

    if cmd == "reply":

        if len(parts) < 3:

            return {

                "text":
                    "فرمت:\nreply TRACKING متن پاسخ",

                "keyboard":
                    EXPERT_MENU,

            }

        tracking = parts[1]

        text = " ".join(parts[2:])

        request = get_request_by_tracking(tracking)

        if not request:

            return {

                "text":
                    "درخواست پیدا نشد.",

                "keyboard":
                    EXPERT_MENU,

            }

        add_message(

            tracking,

            "EXPERT",

            chat_id,

            "TEXT",

            text,

        )

        add_history(

            tracking,

            "EXPERT_REPLY",

            "EXPERT",

            chat_id,

            "پاسخ کارشناس ثبت شد.",

        )

        update_request_status(

            request["id"],

            "ANSWERED",

        )

        return {

            "text":
                "✅ پاسخ ثبت شد.",

            "keyboard":
                EXPERT_MENU,

        }

    return {

        "text":
            "دستور نامعتبر است.",

        "keyboard":
            EXPERT_MENU,

        }
