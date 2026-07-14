"""
handlers/admin_handlers.py

Advanced admin panel handler.
"""

from database import is_admin

from menus import (
    ADMIN_MENU,
    MAIN_MENU,
)

from admin_service import (
    dashboard,
    get_statistics,

    get_daily_report,
    get_weekly_report,
    get_monthly_report,

    get_recent_activity,

    create_expert_account,
    activate_expert,
    deactivate_expert,

    transfer_request,

    add_system_holiday,
    delete_system_holiday,

    update_settings,
)


def handle_admin_message(
    chat_id: int,
    message: str,
):

    if not is_admin(chat_id):
        return {
            "text": "⛔ شما دسترسی به پنل مدیریت ندارید.",
        }


    if message == "/admin":
        return {
            "text": "🛠 پنل مدیریت سامانه",
            "keyboard": ADMIN_MENU,
        }


    if message == "🏠 منوی اصلی":

        return {
            "text": "منوی اصلی",
            "keyboard": MAIN_MENU,
        }


    if not message:

        return {
            "text": "پیام نامعتبر است",
            "keyboard": ADMIN_MENU,
        }


    parts = message.split()

    cmd = parts[0].lower()



    # Dashboard
    if cmd == "dashboard" or message == "📊 داشبورد":

        result = dashboard()

        if not result["success"]:

            return {
                "text": result["message"],
                "keyboard": ADMIN_MENU,
            }


        stats = result["statistics"]

        return {

            "text":
            (
                "📊 داشبورد سامانه\n\n"
                f"📥 درخواست باز: {stats['open']}\n"
                f"✅ بسته شده: {stats['closed']}\n"
                f"🆕 امروز: {stats['today']}\n"
                f"👨‍💼 کارشناسان فعال: {stats['experts']}"
            ),

            "keyboard": ADMIN_MENU,
        }



    # Statistics
    if cmd == "stats" or message == "📈 آمار":

        result = get_statistics()

        if not result["success"]:

            return {
                "text": result["message"],
                "keyboard": ADMIN_MENU,
            }


        stats = result["statistics"]

        return {

            "text":
            (
                "📈 آمار کلی\n\n"
                f"🟢 باز: {stats['open']}\n"
                f"✅ بسته: {stats['closed']}\n"
                f"📅 امروز: {stats['today']}\n"
                f"👨‍💼 کارشناسان: {stats['experts']}"
            ),

            "keyboard": ADMIN_MENU,
        }



    # Reports

    report_map = {

        "📅 گزارش روزانه": get_daily_report,
        "📆 گزارش هفتگی": get_weekly_report,
        "🗓 گزارش ماهانه": get_monthly_report,

    }


    if message in report_map:

        return format_report(
            message,
            report_map[message](),
        )



    # Recent

    if message == "📋 درخواست‌های اخیر":

        result = get_recent_activity()


        if not result["success"]:

            return {
                "text": result["message"],
                "keyboard": ADMIN_MENU,
            }


        text = "📋 آخرین درخواست‌ها\n\n"


        for item in result["recent_requests"]:

            text += (

                f"🎫 {item['tracking_code']}\n"
                f"📌 وضعیت: {item['status']}\n"
                f"🛠 خدمت: {item['service']}\n"
                "────────────\n"

            )


        return {

            "text": text,
            "keyboard": ADMIN_MENU,

        }



    # Create Expert

    if cmd == "create_expert":

        if len(parts) < 5:

            return {

                "text":
                "فرمت:\ncreate_expert chat_id name username department",

                "keyboard": ADMIN_MENU,
            }


        result = create_expert_account(

            int(parts[1]),
            parts[2],
            parts[3],
            parts[4],

        )


        return {

            "text":
            "✅ کارشناس ثبت شد"
            if result["success"]
            else result["message"],

            "keyboard": ADMIN_MENU,

        }



    # Activate

    if cmd == "activate_expert":

        if len(parts) < 2:

            return {
                "text": "فرمت: activate_expert chat_id",
                "keyboard": ADMIN_MENU,
            }


        result = activate_expert(
            int(parts[1])
        )


        return {

            "text":
            "✅ فعال شد"
            if result["success"]
            else result["message"],

            "keyboard": ADMIN_MENU,

        }



    # Deactivate

    if cmd == "deactivate_expert":

        if len(parts) < 2:

            return {
                "text": "فرمت: deactivate_expert chat_id",
                "keyboard": ADMIN_MENU,
            }


        result = deactivate_expert(
            int(parts[1])
        )


        return {

            "text":
            "❌ غیرفعال شد"
            if result["success"]
            else result["message"],

            "keyboard": ADMIN_MENU,

        }



    # Transfer

    if cmd == "transfer":

        if len(parts) < 3:

            return {

                "text":
                "فرمت: transfer request_id expert_id",

                "keyboard": ADMIN_MENU,
            }


        result = transfer_request(
            int(parts[1]),
            int(parts[2]),
        )


        return {

            "text":
            "📤 درخواست منتقل شد"
            if result["success"]
            else result["message"],

            "keyboard": ADMIN_MENU,

        }



    # Holidays

    if cmd == "add_holiday":

        if len(parts) < 2:

            return {
                "text": "فرمت: add_holiday YYYY-MM-DD",
                "keyboard": ADMIN_MENU,
            }


        result = add_system_holiday(parts[1])


        return {

            "text":
            "📅 تعطیلی ثبت شد"
            if result["success"]
            else result["message"],

            "keyboard": ADMIN_MENU,

        }



    if cmd == "remove_holiday":

        if len(parts) < 2:

            return {
                "text": "فرمت: remove_holiday YYYY-MM-DD",
                "keyboard": ADMIN_MENU,
            }


        result = delete_system_holiday(parts[1])


        return {

            "text":
            "📅 تعطیلی حذف شد"
            if result["success"]
            else result["message"],

            "keyboard": ADMIN_MENU,

        }



    # Settings

    if cmd == "set":

        if len(parts) < 3:

            return {

                "text": "فرمت: set key value",
                "keyboard": ADMIN_MENU,

            }


        result = update_settings(

            parts[1],
            " ".join(parts[2:]),

        )


        return {

            "text":
            "⚙️ تنظیم شد"
            if result["success"]
            else result["message"],

            "keyboard": ADMIN_MENU,

        }



    return {

        "text": "❌ دستور نامعتبر است.",

        "keyboard": ADMIN_MENU,

    }



def format_report(
    title: str,
    result: dict,
):

    if not result["success"]:

        return {

            "text": result["message"],

            "keyboard": ADMIN_MENU,

        }


    report = result["report"]


    return {

        "text":
        (
            f"{title}\n\n"
            f"📥 کل درخواست‌ها: {report['total']}\n"
            f"🟢 باز: {report['open']}\n"
            f"✅ بسته: {report['closed']}"
        ),

        "keyboard": ADMIN_MENU,

    }
