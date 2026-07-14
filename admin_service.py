"""
admin_service.py

Business logic for admin operations.
"""

from typing import Dict, Any

from database import (
    create_expert,
    set_active,
    assign_expert,

    add_holiday,
    remove_holiday,

    set_setting,

    get_dashboard_statistics,
    get_recent_requests,

    get_daily_statistics,
    get_weekly_statistics,
    get_monthly_statistics,
)

from logger import (
    log_info,
    log_error,
)


# -------------------------------------------------
# Dashboard
# -------------------------------------------------
def dashboard() -> Dict[str, Any]:

    try:

        return {

            "success": True,

            "statistics":
                get_dashboard_statistics(),

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


# -------------------------------------------------
# Expert Management
# -------------------------------------------------
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


def activate_expert(
    chat_id: int,
):

    return change_expert_status(
        chat_id,
        True,
    )


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


# -------------------------------------------------
# Transfer Request
# -------------------------------------------------
def transfer_request(
    request_id: int,
    expert_id: int,
):

    try:

        assign_expert(
            request_id,
            expert_id,
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


# -------------------------------------------------
# Holiday Management
# -------------------------------------------------
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


# -------------------------------------------------
# Settings
# -------------------------------------------------
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
            "update_settings",
            str(e),
        )

        return {

            "success": False,

            "message":
                "خطا در بروزرسانی تنظیمات",

        }


# -------------------------------------------------
# Statistics
# -------------------------------------------------
def get_statistics():

    result = dashboard()

    if not result["success"]:

        return result

    return {

        "success": True,

        "statistics":
            result["statistics"],

    }


def get_recent_activity(
    limit: int = 10,
):

    try:

        return {

            "success": True,

            "recent_requests":
                get_recent_requests(limit),

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


# -------------------------------------------------
# Reports
# -------------------------------------------------
def get_daily_report():

    try:

        return {

            "success": True,

            "report":
                get_daily_statistics(),

        }

    except Exception as e:

        return {

            "success": False,

            "message":
                "خطا در گزارش روزانه",

        }


def get_weekly_report():

    try:

        return {

            "success": True,

            "report":
                get_weekly_statistics(),

        }

    except Exception:

        return {

            "success": False,

            "message":
                "خطا در گزارش هفتگی",

        }


def get_monthly_report():

    try:

        return {

            "success": True,

            "report":
                get_monthly_statistics(),

        }

    except Exception:

        return {

            "success": False,

            "message":
                "خطا در گزارش ماهانه",

    }
