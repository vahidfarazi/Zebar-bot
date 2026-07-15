"""
database/__init__.py

Central database export layer.
"""


# =====================================================
# CONNECTION
# =====================================================

from .connection import (
    get_connection,
    close_connection,
    init_database,
)


# =====================================================
# SCHEMA
# =====================================================

from .schema import (
    create_tables,
)


# =====================================================
# CRUD CORE
# =====================================================

from .crud import (
    execute,
    fetch_one,
    fetch_all,
)


# =====================================================
# USERS
# =====================================================

from .users import (
    create_user,
    get_user,
    get_all_users,
)


def get_user_by_chat_id(
    chat_id: int,
):
    return get_user(
        chat_id
    )


# =====================================================
# EXPERTS
# =====================================================

from .experts import (
    create_expert,
    get_expert,
    list_experts,
    list_active_experts,
)


def get_active_experts():
    return list_active_experts()


def get_active_expert(
    chat_id: int,
):
    return get_expert(
        chat_id
    )


# =====================================================
# ADMINS
# =====================================================

from .admins import (
    add_admin,
    remove_admin,
    is_admin,
    get_all_admins,
    get_active_admins,
    count_admins,
)


# =====================================================
# REQUESTS
# =====================================================

from .requests import (
    insert_request,
    get_request,
    get_request_by_tracking,
    get_user_requests,
    update_request_status,
    assign_expert,
    transfer_request,
    close_request,
)


# =====================================================
# TRACKING
# =====================================================

from .tracking_sequence import (
    get_next_tracking_number,
)


from .tracking import (
    get_last_tracking_number,
)


def create_tracking_code(
    year: str,
    department_code: str = "SR",
):

    number = get_next_tracking_number(
        year,
        department_code,
    )

    return (
        f"{department_code}-"
        f"{year}-"
        f"{number:07d}"
    )


# =====================================================
# MESSAGES
# =====================================================

from .messages import (
    add_message,
    get_message,
    get_messages,
    get_history,
    get_last_message,
    get_last_user_message,
    get_last_expert_message,
    count_messages,
    get_expert_messages,
    get_user_messages,
    get_expert_message_statistics,
    delete_messages,
)


# =====================================================
# HISTORY
# =====================================================

from .history import (
    add_history,
    get_history as get_request_history,
    get_latest_history,
    count_history,
    add_transfer_history,
    add_status_history,
    add_assignment_history,
    add_admin_history,
    add_expert_history,
    delete_history,
)


# =====================================================
# SETTINGS
# =====================================================

from .settings import (
    get_setting,
    set_setting,
    delete_setting,
    get_all_settings,
    get_working_hours,
)


# =====================================================
# HOLIDAYS
# =====================================================

from .holidays import (
    add_holiday,
    remove_holiday,
    enable_holiday,
    disable_holiday,
    get_holidays,
    get_all_holidays,
    is_holiday,
)


# =====================================================
# LOGS
# =====================================================

from .logs import (
    insert_log,
    get_logs,
    clear_logs,
)


# =====================================================
# STATISTICS
# =====================================================

from .statistics import (
    get_dashboard_statistics,
    get_daily_statistics,
    get_weekly_statistics,
    get_monthly_statistics,
    get_service_statistics,
    get_expert_statistics,
    get_daily_chart_data,
)


# =====================================================
# REPORTS
# =====================================================

from .reports import (
    get_dashboard_report,
)


# =====================================================
# EXPORTS
# =====================================================

__all__ = [

    # connection
    "get_connection",
    "close_connection",
    "init_database",

    # schema
    "create_tables",

    # crud
    "execute",
    "fetch_one",
    "fetch_all",

    # users
    "create_user",
    "get_user",
    "get_user_by_chat_id",
    "get_all_users",

    # experts
    "create_expert",
    "get_expert",
    "get_active_experts",
    "get_active_expert",

    # admins
    "add_admin",
    "remove_admin",
    "is_admin",

    # requests
    "insert_request",
    "get_request",
    "get_request_by_tracking",
    "update_request_status",
    "assign_expert",
    "transfer_request",
    "close_request",

    # tracking
    "create_tracking_code",
    "get_last_tracking_number",
    "get_next_tracking_number",

    # messages
    "add_message",
    "get_message",
    "get_messages",
    "get_history",
    "get_last_message",
    "get_last_user_message",
    "get_last_expert_message",
    "count_messages",
    "get_expert_messages",
    "get_user_messages",
    "get_expert_message_statistics",
    "delete_messages",

    # history
    "add_history",
    "get_request_history",
    "get_latest_history",
    "count_history",
    "add_transfer_history",
    "add_status_history",
    "add_assignment_history",
    "add_admin_history",
    "add_expert_history",
    "delete_history",

    # settings
    "get_setting",
    "set_setting",
    "delete_setting",
    "get_all_settings",
    "get_working_hours",

    # holidays
    "add_holiday",
    "remove_holiday",
    "enable_holiday",
    "disable_holiday",
    "get_holidays",
    "get_all_holidays",
    "is_holiday",

    # logs
    "insert_log",
    "get_logs",
    "clear_logs",

    # statistics
    "get_dashboard_statistics",
    "get_daily_statistics",
    "get_weekly_statistics",
    "get_monthly_statistics",
    "get_service_statistics",
    "get_expert_statistics",
    "get_daily_chart_data",

    # reports
    "get_dashboard_report",
]
