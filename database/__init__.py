"""
database/__init__.py

Database package exports.
"""

# =================================================
# Schema / Initialization
# =================================================

from .schema import (
    init_database,
)


# =================================================
# Connection
# =================================================

from .connection import (
    get_connection,
)


# =================================================
# CRUD Helpers
# =================================================

from .crud import (
    execute,
    fetch_one,
    fetch_all,
    execute_many,
    table_exists,
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
    get_recent_requests,
    get_sla_statistics,
)


# =================================================
# Messages
# =================================================

from .messages import (
    add_message,
    get_message,
    get_messages,
    get_last_message,
    get_last_user_message,
    get_last_expert_message,
    count_messages,
    get_expert_messages,
    get_user_messages,
    get_expert_message_statistics,
    delete_messages,
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
    add_admin,
    remove_admin,
    is_admin,
    get_all_admins,
    count_admins,
    admin_exists,
)


# =================================================
# Users
# =================================================

from .users import (
    create_user,
    get_user,
    update_username,
    update_full_name,
    update_role,
    get_all_users,
)


# =================================================
# Holidays
# =================================================

from .holidays import (
    add_holiday,
    remove_holiday,
    enable_holiday,
    disable_holiday,
    is_holiday,
    get_all_holidays,
    get_holidays,
)


# =================================================
# Logs
# =================================================

from .logs import (
    insert_log,
    get_logs,
    clear_logs,
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
# History
# =================================================

from .history import (
    add_history,
    get_history,
    get_latest_history,
    count_history,
    add_transfer_history,
    add_status_history,
    add_assignment_history,
    add_admin_history,
    add_expert_history,
    delete_history,
)


# =================================================
# Reports
# =================================================

from .reports import (
    normalize_statistics,
    get_daily_statistics,
    get_weekly_statistics,
    get_monthly_statistics,
    get_daily_chart_data,
    get_service_statistics,
    get_expert_statistics,
    get_dashboard_report,
)


# =================================================
# Dashboard
# =================================================

from .dashboard import (
    get_dashboard_statistics,
    get_dashboard,
    get_sla_dashboard,
)


# =================================================
# Package Version
# =================================================

__all__ = [

    # schema
    "init_database",

    # connection
    "get_connection",

    # crud
    "execute",
    "fetch_one",
    "fetch_all",
    "execute_many",
    "table_exists",

    # requests
    "insert_request",
    "get_request",
    "get_request_by_tracking",
    "get_user_requests",
    "update_request_status",
    "assign_expert",
    "transfer_request",
    "close_request",
    "get_recent_requests",
    "get_sla_statistics",

    # messages
    "add_message",
    "get_messages",
    "delete_messages",

    # experts
    "create_expert",
    "get_expert",
    "list_experts",
    "delete_expert",

    # admins
    "add_admin",
    "remove_admin",
    "is_admin",

    # users
    "create_user",
    "get_user",

    # holidays
    "add_holiday",
    "remove_holiday",
    "get_holidays",

    # logs
    "insert_log",
    "get_logs",
    "clear_logs",

    # tracking
    "get_last_tracking_number",
    "get_next_tracking_number",

    # history
    "add_history",
    "get_history",
    "delete_history",

    # reports
    "get_dashboard_report",

    # dashboard
    "get_dashboard_statistics",
    "get_dashboard",
    "get_sla_dashboard",

]
