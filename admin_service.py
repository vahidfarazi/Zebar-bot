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


# -----------------------------
# Dashboard
# -----------------------------
def dashboard() -> Dict[str, Any]:
    """
    Return dashboard statistics.
    """

    try:

        stats = get_dashboard_statistics()

        recent = get_recent_requests(10)

        return {

            "success": True,

            "statistics": stats,

            "recent_requests": recent,

        }

    except Exception as e:

        log_error(

            "admin_service",

            "dashboard",

            str(e),

        )

        return {

            "success": False,

            "message": "خطا در دریافت اطلاعات داشبورد",

        }


# -----------------------------
# Expert Management
# -----------------------------
def create_expert_account(
    chat_id: int,
    name: str,
    username: str,
    department: str,
) -> Dict[str, Any]:
    """
    Create or update expert account.
    """

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
            "message": "خطا در ایجاد کارشناس",
        }
        
# -----------------------------
# Deactivate Expert
# -----------------------------
def deactivate_expert(
    chat_id: int,
) -> Dict[str, Any]:
    """
    Deactivate expert.
    """

    try:

        set_active(
            chat_id,
            False,
        )

        log_info(
            "admin_service",
            "deactivate_expert",
            str(chat_id),
        )

        return {
            "success": True,
        }

    except Exception as e:

        log_error(
            "admin_service",
            "deactivate_expert",
            str(e),
        )

        return {
            "success": False,
            "message": "خطا در غیرفعال‌سازی کارشناس",
        }


# -----------------------------
# Transfer Request
# -----------------------------
def transfer_request(
    request_id: int,
    expert_id: int,
) -> Dict[str, Any]:
    """
    Transfer request to expert.
    """

    try:

        assign_expert(
            request_id,
            expert_id,
        )

        log_info(
            "admin_service",
            "transfer_request",
            f"{request_id} -> {expert_id}",
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
            "message": "خطا در انتقال درخواست",
        }


# -----------------------------
# Holiday Management
# -----------------------------
def add_system_holiday(
    date: str,
) -> Dict[str, Any]:
    """
    Add holiday.
    """

    try:

        add_holiday(date)

        log_info(
            "admin_service",
            "add_holiday",
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
            "message": "خطا در ثبت تعطیلی",
        }


def delete_system_holiday(
    date: str,
) -> Dict[str, Any]:
    """
    Remove holiday.
    """

    try:

        remove_holiday(date)

        log_info(
            "admin_service",
            "remove_holiday",
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
            "message": "خطا در حذف تعطیلی",
        }
        
# -----------------------------
# Settings
# -----------------------------
def update_settings(
    key: str,
    value: str,
) -> Dict[str, Any]:
    """
    Update system settings.
    """

    try:

        set_setting(
            key,
            value,
        )

        log_info(
            "admin_service",
            "update_settings",
            f"{key}={value}",
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
            "message": "خطا در بروزرسانی تنظیمات",
        }


# -----------------------------
# Dashboard Helpers
# -----------------------------
def get_dashboard() -> Dict[str, Any]:
    """
    Return dashboard information.
    """

    return dashboard()


def get_statistics() -> Dict[str, Any]:
    """
    Return only dashboard statistics.
    """

    result = dashboard()

    if not result["success"]:

        return result

    return {

        "success": True,

        "statistics": result["statistics"],

    }


def get_recent_activity(
    limit: int = 10,
) -> Dict[str, Any]:
    """
    Return recent requests.
    """

    try:

        return {

            "success": True,

            "recent_requests": get_recent_requests(limit),

        }

    except Exception as e:

        log_error(

            "admin_service",

            "recent_activity",

            str(e),

        )

        return {

            "success": False,

            "message": "خطا در دریافت فعالیت‌های اخیر",

        }

# -----------------------------
# Daily Report
# -----------------------------
def get_daily_report():

    try:

        return {
            "success": True,
            "report": get_daily_statistics(),
        }

    except Exception as e:

        log_error(
            "admin_service",
            "daily_report",
            str(e),
        )

        return {
            "success": False,
            "message": "خطا در گزارش روزانه",
        }


# -----------------------------
# Weekly Report
# -----------------------------
def get_weekly_report():

    try:

        return {
            "success": True,
            "report": get_weekly_statistics(),
        }

    except Exception as e:

        log_error(
            "admin_service",
            "weekly_report",
            str(e),
        )

        return {
            "success": False,
            "message": "خطا در گزارش هفتگی",
        }


# -----------------------------
# Monthly Report
# -----------------------------
def get_monthly_report():

    try:

        return {
            "success": True,
            "report": get_monthly_statistics(),
        }

    except Exception as e:

        log_error(
            "admin_service",
            "monthly_report",
            str(e),
        )

        return {
            "success": False,
            "message": "خطا در گزارش ماهانه",
        }
