"""
database

Central database package for Azarakhsh.
Exports all public database functions.
"""


# =================================================
# Connection
# =================================================

from .connection import (
    get_connection,
)


# =================================================
# Schema
# =================================================

from .schema import (
    init_database,
)


# =================================================
# CRUD
# =================================================

from .crud import (
    execute,
    execute_many,
    fetch_one,
    fetch_all,
    table_exists,
)


# =================================================
# Settings
# =================================================

from .settings import (
    get_setting,
    set_setting,
)


# =================================================
# Requests
# =================================================

from .requests import (

    insert_request,

    get_request,

    get_request_by_tracking,

    get_user_requests,

    update_request_status,

    assign_expert,

    transfer_request,

    get_transferred_requests,

    get_expert_requests,

    save_expert_message,

    close_request,

    update_priority,

    delete_request,

    get_recent_requests,

)


# =================================================
# Reports
# =================================================

from .reports import (

    get_daily_statistics,

    get_weekly_statistics,

    get_monthly_statistics,

    get_daily_chart_data,

    get_service_statistics,

    get_expert_statistics,

    get_dashboard_report,

)


# =================================================
# Messages
# =================================================

from .messages import (

    add_message,

    get_message,

    get_messages,

    get_last_message,

    count_messages,

    get_expert_messages,

    get_user_messages,

    delete_messages,

)


# =================================================
# History
# =================================================

from .history import (

    add_history,

    get_history,

    count_history,

    add_transfer_history,

    add_status_history,

    add_assignment_history,

    add_admin_history,

    add_expert_history,

    get_latest_history,

    delete_history,

)


# =================================================
# Tracking
# =================================================

from .tracking import (
    get_last_tracking_number,
)


from .tracking_sequence import (
    get_next_tracking_number,
)


# =================================================
# Users
# =================================================

from .users import (

    get_user,

    create_user,

)


# =================================================
# Experts
# =================================================

from .experts import (

    create_expert,

    get_expert,

    list_experts,

    list_active_experts,

    update_department,

    set_active,

    activate_expert,

    deactivate_expert,

    delete_expert,

    count_experts,

    expert_exists,

)


# =================================================
# Admins
# =================================================

from .admins import (

    is_admin,

    add_admin,

    remove_admin,

    get_all_admins,

)


# =================================================
# Holidays
# =================================================

from .holidays import (

    is_holiday,

    add_holiday,

    remove_holiday,

    enable_holiday,

    disable_holiday,

    get_all_holidays,

)


# =================================================
# Logs
# =================================================

from .logs import (

    insert_log,

)


__all__ = [

    # Connection
    "get_connection",

    # Schema
    "init_database",

    # CRUD
    "execute",
    "execute_many",
    "fetch_one",
    "fetch_all",
    "table_exists",

    # Settings
    "get_setting",
    "set_setting",

    # Requests
    "insert_request",
    "get_request",
    "get_request_by_tracking",
    "get_user_requests",
    "update_request_status",
    "assign_expert",
    "transfer_request",
    "get_transferred_requests",
    "get_expert_requests",
    "save_expert_message",
    "close_request",
    "update_priority",
    "delete_request",
    "get_recent_requests",

    # Reports
    "get_daily_statistics",
    "get_weekly_statistics",
    "get_monthly_statistics",
    "get_daily_chart_data",
    "get_service_statistics",
    "get_expert_statistics",
    "get_dashboard_report",

    # Messages
    "add_message",
    "get_message",
    "get_messages",
    "get_last_message",
    "count_messages",
    "get_expert_messages",
    "get_user_messages",
    "delete_messages",

    # History
    "add_history",
    "get_history",
    "count_history",
    "add_transfer_history",
    "add_status_history",
    "add_assignment_history",
    "add_admin_history",
    "add_expert_history",
    "get_latest_history",
    "delete_history",

    # Tracking
    "get_last_tracking_number",
    "get_next_tracking_number",

    # Users
    "get_user",
    "create_user",

    # Experts
    "create_expert",
    "get_expert",
    "list_experts",
    "list_active_experts",
    "update_department",
    "set_active",
    "activate_expert",
    "deactivate_expert",
    "delete_expert",
    "count_experts",
    "expert_exists",

    # Admins
    "is_admin",
    "add_admin",
    "remove_admin",
    "get_all_admins",

    # Holidays
    "is_holiday",
    "add_holiday",
    "remove_holiday",
    "enable_holiday",
    "disable_holiday",
    "get_all_holidays",

    # Logs
    "insert_log",

]
