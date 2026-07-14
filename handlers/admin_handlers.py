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
    update_working_hours,
    update_working_days,
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

                f"📥 باز: {stats.get('open',0)}\n"
                f"⏳ در انتظار: {stats.get('pending',0)}\n"
                f"🔄 منتقل شده: {stats.get('transferred',0)}\n"
                f"✅ بسته: {stats.get('closed',0)}\n\n"

                f"📅 وضعیت کاری: {result.get('working_status','-')}"
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

                f"🟢 باز: {stats.get('open',0)}\n"
                f"⏳ انتظار: {stats.get('pending',0)}\n"
                f"🔄 انتقال: {stats.get('transferred',0)}\n"
                f"✅ بسته: {stats.get('closed',0)}"
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
                f"🎫 {item.get('tracking_code')}\n"
                f"📌 {item.get('status')}\n"
                f"🛠 {item.get('service')}\n"
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
                "create_expert chat_id name username department",
                "keyboard": ADMIN_MENU,
            }


        result = create_expert_account(
            int(parts[1]),
            parts[2],
            parts[3],
            parts[4],
        )


        return action_result(result)



    # Activate

    if cmd == "activate_expert":

        result = activate_expert(
            int(parts[1])
        )

        return action_result(result)



    # Deactivate

    if cmd == "deactivate_expert":

        result = deactivate_expert(
            int(parts[1])
        )

        return action_result(result)



    # Transfer

    if cmd == "transfer":

        result = transfer_request(
            int(parts[1]),
            int(parts[2]),
        )

        return action_result(result)



    # Holiday

    if cmd == "add_holiday":

        result = add_system_holiday(
            parts[1]
        )

        return action_result(result)



    if cmd == "remove_holiday":

        result = delete_system_holiday(
            parts[1]
        )

        return action_result(result)



    # Working Hours

    if cmd == "worktime":

        result = update_working_hours(
            parts[1],
            parts[2],
        )

        return action_result(result)



    if cmd == "workdays":

        result = update_working_days(
            parts[1]
        )

        return action_result(result)



    # Settings

    if cmd == "set":

        result = update_settings(
            parts[1],
            " ".join(parts[2:]),
        )

        return action_result(result)



    return {
        "text": "❌ دستور نامعتبر است.",
        "keyboard": ADMIN_MENU,
    }



def action_result(result):

    return {

        "text":
        "✅ انجام شد"
        if result["success"]
        else result["message"],

        "keyboard": ADMIN_MENU,

    }



def format_report(
    title:str,
    result:dict,
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

            f"📥 کل: {report.get('total',0)}\n"
            f"🟢 باز: {report.get('open',0)}\n"
            f"⏳ انتظار: {report.get('pending',0)}\n"
            f"🔄 انتقال: {report.get('transferred',0)}\n"
            f"✅ بسته: {report.get('closed',0)}"
        ),

        "keyboard": ADMIN_MENU,

        }
