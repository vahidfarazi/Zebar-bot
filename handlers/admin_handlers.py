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


from date_utils import (

    today_jalali,

    previous_day,
    next_day,

    previous_jalali_month,
    next_jalali_month,

    current_week_range,
    previous_week_range,
    next_week_range,

)


from calendar_utils import (

    open_calendar,

)



# =================================================
# Main Admin Handler
# =================================================


def handle_admin_message(
    chat_id: int,
    message: str,
):


    if not is_admin(chat_id):

        return {

            "text":
                "⛔ شما دسترسی به پنل مدیریت ندارید.",

        }



    if message == "/admin":

        return {

            "text":
                "🛠 پنل مدیریت سامانه",

            "keyboard":
                ADMIN_MENU,

        }



    if message == "🏠 منوی اصلی":

        return {

            "text":
                "منوی اصلی",

            "keyboard":
                MAIN_MENU,

        }



    if not message:

        return {

            "text":
                "پیام نامعتبر است",

            "keyboard":
                ADMIN_MENU,

        }



    parts = message.split()

    cmd = parts[0].lower()



    # =================================================
    # Dashboard
    # =================================================


    if cmd == "dashboard" or message == "📊 داشبورد":


        result = dashboard()



        if not result["success"]:

            return {

                "text":
                    result["message"],

                "keyboard":
                    ADMIN_MENU,

            }



        stats = result["statistics"]


        work = result.get(
            "working_status",
            {},
        )



        return {

            "text":

            (

                "📊 داشبورد سامانه\n\n"

                f"📥 کل: {stats.get('total',0)}\n"

                f"🟢 باز: {stats.get('open',0)}\n"

                f"⏳ در انتظار: {stats.get('pending',0)}\n"

                f"🔄 منتقل شده: {stats.get('transferred',0)}\n"

                f"✅ بسته: {stats.get('closed',0)}\n\n"

                f"⏰ وضعیت کاری: {work.get('message','-')}"

            ),

            "keyboard":
                ADMIN_MENU,

        }



    # =================================================
    # Statistics
    # =================================================


    if cmd == "stats" or message == "📈 آمار":


        result = get_statistics()



        if not result["success"]:

            return {

                "text":
                    result["message"],

                "keyboard":
                    ADMIN_MENU,

            }



        stats = result["statistics"]



        return {

            "text":

            (

                "📈 آمار کلی\n\n"

                f"📌 کل: {stats.get('total',0)}\n"

                f"🟢 باز: {stats.get('open',0)}\n"

                f"⏳ انتظار: {stats.get('pending',0)}\n"

                f"🔄 انتقال: {stats.get('transferred',0)}\n"

                f"✅ بسته: {stats.get('closed',0)}"

            ),

            "keyboard":
                ADMIN_MENU,

        }



    # =================================================
    # Reports
    # =================================================


    if message == "📅 امروز":

        return format_report(

            "📅 گزارش امروز",

            get_daily_report(),

        )



    if message == "⬅️ روز قبل":

        date = previous_day(

            today_jalali(),

        )

        return format_report(

            f"📅 {date}",

            get_daily_report(date),

        )



    if message == "➡️ روز بعد":

        date = next_day(

            today_jalali(),

        )

        return format_report(

            f"📅 {date}",

            get_daily_report(date),

        )



    if message == "📆 این هفته":

        start_date, end_date = current_week_range()

        return format_report(

            f"📆 هفته جاری\n{start_date} تا {end_date}",

            get_weekly_report(

                start_date,

                end_date,

            ),

        )



    if message == "⬅️ هفته قبل":

        start_date, end_date = previous_week_range()

        return format_report(

            f"📆 هفته قبل\n{start_date} تا {end_date}",

            get_weekly_report(

                start_date,

                end_date,

            ),

        )



    if message == "➡️ هفته بعد":

        start_date, end_date = next_week_range()

        return format_report(

            f"📆 هفته بعد\n{start_date} تا {end_date}",

            get_weekly_report(

                start_date,

                end_date,

            ),

        )



    if message == "📅 انتخاب تاریخ":

        return open_calendar()

    if message == "🗓 این ماه":

        today = today_jalali()

        year, month, _ = today.split("/")


        return format_report(

            "🗓 گزارش ماه جاری",

            get_monthly_report(

                int(year),

                int(month),

            ),

        )



    if message == "⬅️ ماه قبل":

        today = today_jalali()

        year, month, _ = today.split("/")


        year, month = previous_jalali_month(

            int(year),

            int(month),

        )


        return format_report(

            "🗓 گزارش ماه قبل",

            get_monthly_report(

                year,

                month,

            ),

        )



    if message == "➡️ ماه بعد":

        today = today_jalali()

        year, month, _ = today.split("/")


        year, month = next_jalali_month(

            int(year),

            int(month),

        )


        return format_report(

            "🗓 گزارش ماه بعد",

            get_monthly_report(

                year,

                month,

            ),

        )



    # =================================================
    # Selected Date From Calendar / Manual
    # =================================================


    if (
        "/" in message
        and len(message.split("/")) == 3
    ):

        try:

            year, month, day = map(

                int,

                message.split("/"),

            )


            if (

                1300 <= year <= 1500

                and 1 <= month <= 12

                and 1 <= day <= 31

            ):


                return format_report(

                    f"📅 گزارش تاریخ {message}",

                    get_daily_report(

                        message,

                    ),

                )


        except Exception:

            pass



    # =================================================
    # Recent Requests
    # =================================================


    if message == "📋 درخواست‌های اخیر":


        result = get_recent_activity()



        if not result["success"]:

            return {

                "text":
                    result["message"],

                "keyboard":
                    ADMIN_MENU,

            }



        text = "📋 آخرین درخواست‌ها\n\n"



        for item in result["recent_requests"]:


            text += (

                f"🎫 {item.get('tracking_code','-')}\n"

                f"📌 وضعیت: {item.get('status','-')}\n"

                f"🛠 خدمت: {item.get('service','-')}\n"

                "────────────\n"

            )



        return {

            "text":

                text,

            "keyboard":

                ADMIN_MENU,

        }



    # =================================================
    # Create Expert
    # =================================================


    if cmd == "create_expert":


        if len(parts) < 5:

            return invalid_command()



        return action_result(

            create_expert_account(

                int(parts[1]),

                parts[2],

                parts[3],

                parts[4],

            )

        )



    # =================================================
    # Activate Expert
    # =================================================


    if cmd == "activate_expert":


        if len(parts) < 2:

            return invalid_command()



        return action_result(

            activate_expert(

                int(parts[1]),

            )

        )



    # =================================================
    # Deactivate Expert
    # =================================================


    if cmd == "deactivate_expert":


        if len(parts) < 2:

            return invalid_command()



        return action_result(

            deactivate_expert(

                int(parts[1]),

            )

        )



    # =================================================
    # Transfer
    # =================================================


    if cmd == "transfer":


        if len(parts) < 3:

            return invalid_command()



        return action_result(

            transfer_request(

                int(parts[1]),

                int(parts[2]),

                chat_id,

            )

        )



    # =================================================
    # Holidays
    # =================================================


    if cmd == "add_holiday":


        if len(parts) < 2:

            return invalid_command()



        return action_result(

            add_system_holiday(

                parts[1],

            )

        )



    if cmd == "remove_holiday":


        if len(parts) < 2:

            return invalid_command()



        return action_result(

            delete_system_holiday(

                parts[1],

            )

        )



    # =================================================
    # Working Time
    # =================================================


    if cmd == "worktime":


        if len(parts) < 3:

            return invalid_command()



        return action_result(

            update_working_hours(

                parts[1],

                parts[2],

            )

        )



    if cmd == "workdays":


        if len(parts) < 2:

            return invalid_command()



        return action_result(

            update_working_days(

                parts[1],

            )

        )



    # =================================================
    # Settings
    # =================================================


    if cmd == "set":


        if len(parts) < 3:

            return invalid_command()



        return action_result(

            update_settings(

                parts[1],

                " ".join(parts[2:]),

            )

        )



    return {

        "text":

            "❌ دستور نامعتبر است.",


        "keyboard":

            ADMIN_MENU,

    }



# =================================================
# Helpers
# =================================================


def action_result(
    result: dict,
):

    return {

        "text":

            "✅ انجام شد"

            if result.get("success")

            else result.get(

                "message",

                "خطا",

            ),


        "keyboard":

            ADMIN_MENU,

    }



def invalid_command():

    return {

        "text":

            "❌ پارامترهای دستور ناقص است.",


        "keyboard":

            ADMIN_MENU,

    }



def format_report(
    title: str,
    result: dict,
):


    if not result.get("success"):

        return {

            "text":

                result.get(

                    "message",

                    "خطا",

                ),

            "keyboard":

                ADMIN_MENU,

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


        "keyboard":

            ADMIN_MENU,

            }
