"""
handlers/admin_handlers.py

Advanced admin panel handler (Phase 1 Dashboard Base).

Features:
- Dashboard
- Daily / Weekly / Monthly statistics
- Expert management
- Request transfer
- Holiday management
- Working hours settings
"""

from database import (
    is_admin,
)

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

    create_expert_account,
    activate_expert,
    deactivate_expert,

    transfer_request,

    add_system_holiday,
    delete_system_holiday,

    update_settings,

    get_recent_activity,
)


# ----------------------------------
# Admin Handler
# ----------------------------------
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



    # ===============================
    # Dashboard
    # ===============================

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



    # ===============================
    # Statistics
    # ===============================

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



    # ===============================
    # Reports
    # ===============================

    if message == "📅 گزارش روزانه":


        result = get_daily_report()

        return format_report(

            "📅 گزارش روزانه",

            result,

        )



    if message == "📆 گزارش هفتگی":


        result = get_weekly_report()

        return format_report(

            "📆 گزارش هفتگی",

            result,

        )



    if message == "🗓 گزارش ماهانه":


        result = get_monthly_report()

        return format_report(

            "🗓 گزارش ماهانه",

            result,

        )



    # ===============================
    # Recent Requests
    # ===============================

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



    # ===============================
    # Create Expert
    # ===============================

    if cmd == "create_expert":


        if len(parts) < 5:

            return {

                "text":

                "فرمت:\n"
                "create_expert chat_id name username department",

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



    # ===============================
    # Activate Expert
    # ===============================

    if cmd == "activate_expert":


        result = activate_expert(

            int(parts[1]),

        )


        return {

            "text":

            "✅ فعال شد"

            if result["success"]

            else result["message"],

            "keyboard": ADMIN_MENU,

        }



    # ===============================
    # Deactivate Expert
    # ===============================

    if cmd == "deactivate_expert":


        result = deactivate_expert(

            int(parts[1]),

        )


        return {

            "text":

            "❌ غیرفعال شد"

            if result["success"]

            else result["message"],

            "keyboard": ADMIN_MENU,

        }



    # ===============================
    # Transfer
    # ===============================

    if cmd == "transfer":


        if len(parts) < 3:

            return {

                "text":

                "فرمت:\ntransfer request_id expert_id",

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



    # ===============================
    # Holidays
    # ===============================

    if cmd == "add_holiday":


        result = add_system_holiday(

            parts[1],

        )


        return {

            "text": "📅 تعطیلی ثبت شد",

            "keyboard": ADMIN_MENU,

        }



    if cmd == "remove_holiday":


        result = delete_system_holiday(

            parts[1],

        )


        return {

            "text": "📅 تعطیلی حذف شد",

            "keyboard": ADMIN_MENU,

        }



    # ===============================
    # Settings
    # ===============================

    if cmd == "set":


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



# ----------------------------------
# Report Formatter
# ----------------------------------

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
