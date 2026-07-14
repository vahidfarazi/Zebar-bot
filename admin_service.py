"""
admin_service.py

Business logic for admin operations.
"""

from typing import Dict, Any


from database import (

    create_expert,

    set_active,

    assign_expert,

    get_request,

    add_holiday,

    remove_holiday,

    set_setting,

    get_setting,


    # Dashboard

    get_dashboard_summary,

    get_dashboard_report,

    get_recent_requests,


    # Reports

    get_daily_statistics,

    get_weekly_statistics,

    get_monthly_statistics,


    add_transfer_history,

)


from working_hours import (
    get_work_status,
)


from logger import (
    log_info,
    log_error,
)



# =================================================
# Dashboard
# =================================================

def dashboard() -> Dict[str, Any]:

    try:

        return {

            "success": True,


            "statistics":

                get_dashboard_summary(),



            "report":

                get_dashboard_report(),



            "working_status":

                get_work_status(),



            "recent_requests":

                get_recent_requests(10),

        }


    except Exception as e:


        log_error(

            "admin_service",

            "dashboard",

            str(e),

        )


        return {

            "success": False,

            "message":

                "خطا در دریافت اطلاعات داشبورد",

        }



# =================================================
# Experts
# =================================================

def create_expert_account(
    chat_id: int,
    name: str,
    username: str,
    department: str,
):

    try:


        create_expert(

            chat_id,

            name,

            username,

            department,

        )


        log_info(

            "admin_service",

            "create_expert",

            str(chat_id),

        )


        return {

            "success": True,

        }



    except Exception as e:


        log_error(

            "admin_service",

            "create_expert",

            str(e),

        )


        return {

            "success": False,

            "message":

                "خطا در ایجاد کارشناس",

        }



# -------------------------------------------------
# Activate
# -------------------------------------------------

def activate_expert(
    chat_id: int,
):

    return change_expert_status(

        chat_id,

        True,

    )



# -------------------------------------------------
# Deactivate
# -------------------------------------------------

def deactivate_expert(
    chat_id: int,
):

    return change_expert_status(

        chat_id,

        False,

    )



def change_expert_status(
    chat_id: int,
    active: bool,
):

    try:


        set_active(

            chat_id,

            active,

        )


        log_info(

            "admin_service",

            "expert_status",

            f"{chat_id}:{active}",

        )


        return {

            "success": True,

        }



    except Exception as e:


        log_error(

            "admin_service",

            "expert_status",

            str(e),

        )


        return {

            "success": False,

            "message":

                "خطا در تغییر وضعیت کارشناس",

        }



# =================================================
# Transfer Request
# =================================================

def transfer_request(
    request_id: int,
    expert_id: int,
    admin_id: int = 0,
):

    try:


        request = get_request(

            request_id,

        )


        if not request:


            return {

                "success": False,

                "message":

                    "درخواست پیدا نشد.",

            }



        old_expert = request.get(

            "expert_id",

        )



        assign_expert(

            request_id,

            expert_id,

        )



        add_transfer_history(

            request["tracking_code"],

            old_expert,

            expert_id,

            admin_id,

        )



        log_info(

            "admin_service",

            "transfer_request",

            f"{request_id}->{expert_id}",

        )



        return {

            "success": True,

        }



    except Exception as e:


        log_error(

            "admin_service",

            "transfer_request",

            str(e),

        )


        return {

            "success": False,

            "message":

                "خطا در انتقال درخواست",

        }



# =================================================
# Holidays
# =================================================

def add_system_holiday(
    date: str,
):

    try:


        add_holiday(

            date,

        )


        return {

            "success": True,

        }



    except Exception as e:


        log_error(

            "admin_service",

            "add_holiday",

            str(e),

        )


        return {

            "success": False,

            "message":

                "خطا در ثبت تعطیلی",

        }



def delete_system_holiday(
    date: str,
):

    try:


        remove_holiday(

            date,

        )


        return {

            "success": True,

        }



    except Exception as e:


        log_error(

            "admin_service",

            "remove_holiday",

            str(e),

        )


        return {

            "success": False,

            "message":

                "خطا در حذف تعطیلی",

        }



# =================================================
# Working Hours
# =================================================

def update_working_hours(
    start: str,
    end: str,
):

    try:


        set_setting(

            "WORK_START",

            start,

        )


        set_setting(

            "WORK_END",

            end,

        )


        return {

            "success": True,

        }



    except Exception as e:


        log_error(

            "admin_service",

            "working_hours",

            str(e),

        )


        return {

            "success": False,

            "message":

                "خطا در تغییر ساعات کاری",

        }



def update_working_days(
    days: str,
):

    try:


        set_setting(

            "WORKING_DAYS",

            days,

        )


        return {

            "success": True,

        }



    except Exception as e:


        log_error(

            "admin_service",

            "working_days",

            str(e),

        )


        return {

            "success": False,

            "message":

                "خطا در تغییر روزهای کاری",

        }



def get_working_hours():

    return {


        "start":

            get_setting(

                "WORK_START",

            )

            or "07:00",



        "end":

            get_setting(

                "WORK_END",

            )

            or "13:00",



        "days":

            get_setting(

                "WORKING_DAYS",

            )

            or "0,1,2,3,4",


    }



# =================================================
# Settings
# =================================================

def update_settings(
    key: str,
    value: str,
):

    try:


        set_setting(

            key,

            value,

        )


        return {

            "success": True,

        }



    except Exception as e:


        log_error(

            "admin_service",

            "settings",

            str(e),

        )


        return {

            "success": False,

            "message":

                "خطا در بروزرسانی تنظیمات",

        }



# =================================================
# Statistics
# =================================================

def get_statistics():

    result = dashboard()



    if not result["success"]:

        return result



    return {

        "success": True,

        "statistics":

            result["statistics"],

    }



# =================================================
# Recent Activity
# =================================================

def get_recent_activity(
    limit: int = 10,
):

    try:


        return {

            "success": True,

            "recent_requests":

                get_recent_requests(

                    limit,

                ),

        }



    except Exception as e:


        log_error(

            "admin_service",

            "recent_activity",

            str(e),

        )


        return {

            "success": False,

            "message":

                "خطا در دریافت درخواست‌ها",

        }



# =================================================
# Reports
# =================================================

def get_daily_report():

    return {

        "success": True,

        "report":

            get_daily_statistics(),

    }



def get_weekly_report():

    return {

        "success": True,

        "report":

            get_weekly_statistics(),

    }



def get_monthly_report():

    return {

        "success": True,

        "report":

            get_monthly_statistics(),

        }
