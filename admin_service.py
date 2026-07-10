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
)

from logger import (
    log_info,
    log_error,
)


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
# Dashboard Statistics
# -----------------------------
def get_dashboard_statistics() -> Dict[str, Any]:
    """
    Return dashboard statistics.
    """

    try:

        from database import (
            get_dashboard_statistics,
        )

        return {

            "success": True,

            "data": get_dashboard_statistics(),

        }

    except Exception as e:

        log_error(

            "admin_service",

            "dashboard_statistics",

            str(e),

        )

        return {

            "success": False,

            "message": "خطا در دریافت آمار",

        }


# -----------------------------
# Recent Requests
# -----------------------------
def get_recent_requests(
    limit: int = 20,
) -> Dict[str, Any]:
    """
    Return latest requests.
    """

    try:

        from database import (
            get_recent_requests,
        )

        return {

            "success": True,

            "data": get_recent_requests(limit),

        }

    except Exception as e:

        log_error(

            "admin_service",

            "recent_requests",

            str(e),

        )

        return {

            "success": False,

            "message": "خطا در دریافت درخواست‌ها",

        }


# -----------------------------
# Request Details
# -----------------------------
def get_request_details(
    tracking_code: str,
) -> Dict[str, Any]:
    """
    Return complete request details.
    """

    try:

        from database import (

            get_request_by_tracking,

            get_messages,

            get_history,

        )

        request = get_request_by_tracking(
            tracking_code,
        )

        if not request:

            return {

                "success": False,

                "message": "درخواست یافت نشد.",

            }

        return {

            "success": True,

            "request": request,

            "messages": get_messages(
                tracking_code,
            ),

            "history": get_history(
                tracking_code,
            ),

        }

    except Exception as e:

        log_error(

            "admin_service",

            "request_details",

            str(e),

        )

        return {

            "success": False,

            "message": "خطا در دریافت اطلاعات",

    }
