"""
database package exports
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
    create_tables,
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
    column_exists,
)

# =================================================
# Users
# =================================================

from .users import (
    create_user,
    get_user,
    get_user_by_chat_id,
    update_username,
    update_full_name,
    update_role,
    delete_user,
    user_exists,
    get_all_users,
    get_users,
    count_users,
)

# =================================================
# Experts
# =================================================

from .experts import (
    create_expert,
    get_expert,
    expert_exists,
    list_experts,
    list_active_experts,
    get_active_experts,
    get_active_expert,
    update_department,
    update_phone,
    set_active,
    activate_expert,
    deactivate_expert,
    delete_expert,
    count_experts,
)

# =================================================
# Requests
# =================================================

from .requests import (
    insert_request,
    get_request,
    get_request_by_tracking,
    get_request_by_code,
    request_exists,
    get_user_requests,
    get_requests,
    get_expert_requests,
    update_request_status,
    assign_expert,
    transfer_request,
    save_expert_message,
    close_request,
    reopen_request,
    update_priority,
    delete_request,
    get_recent_requests,
    get_transferred_requests,
    count_requests,
    count_open_requests,
    count_pending_requests,
    count_closed_requests,
    count_expert_requests,
    get_sla_statistics,
    get_requests_summary,
)

# =================================================
# Messages
# =================================================

from .messages import (
    add_message,
    get_message,
    message_exists,
    get_messages,
    get_request_messages,
    get_history as get_message_history,
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
# History
# =================================================

from .history import (
    add_history,
    get_history,
    get_request_history,
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
# Holidays
# =================================================

from .holidays import (
    add_holiday,
    remove_holiday,
    is_holiday,
    get_holidays,
)

# =================================================
# Settings
# =================================================

from .settings import (
    get_setting,
    set_setting,
    delete_setting,
    setting_exists,
    get_all_settings,
)

# =================================================
# Tracking
# =================================================

from .tracking import (
    generate_tracking_code,
    get_next_tracking_number,
)

# =================================================
# Dashboard
# =================================================

from .dashboard import (
    get_dashboard,
    get_dashboard_statistics,
    get_dashboard_summary,
    get_service_statistics,
    get_daily_chart_data,
    get_expert_statistics,
    get_recent_activity,
    get_sla_dashboard,
)

# =================================================
# Reports
# =================================================

from .reports import (
    normalize_statistics,
    get_daily_statistics,
    get_weekly_statistics,
    get_monthly_statistics,
    get_dashboard_report,
    get_reports,
)

# =================================================
# Public API
# =================================================

__all__ = [

    # connection
    "get_connection",

    # crud
    "execute",
    "execute_many",
    "fetch_one",
    "fetch_all",
    "table_exists",
    "column_exists",

    # users
    "create_user",
    "get_user",
    "get_user_by_chat_id",
    "update_username",
    "update_full_name",
    "update_role",
    "delete_user",
    "user_exists",
    "get_all_users",
    "get_users",
    "count_users",

    # experts
    "create_expert",
    "get_expert",
    "expert_exists",
    "list_experts",
    "list_active_experts",
    "get_active_experts",
    "get_active_expert",
    "update_department",
    "update_phone",
    "set_active",
    "activate_expert",
    "deactivate_expert",
    "delete_expert",
    "count_experts",

    # requests
    "insert_request",
    "get_request",
    "get_request_by_tracking",
    "get_request_by_code",
    "request_exists",
    "get_user_requests",
    "get_requests",
    "get_expert_requests",
    "update_request_status",
    "assign_expert",
    "transfer_request",
    "save_expert_message",
    "close_request",
    "reopen_request",
    "update_priority",
    "delete_request",
    "get_recent_requests",
    "get_transferred_requests",
    "count_requests",
    "count_open_requests",
    "count_pending_requests",
    "count_closed_requests",
    "count_expert_requests",
    "get_sla_statistics",
    "get_requests_summary",

    # messages
    "add_message",
    "get_message",
    "message_exists",
    "get_messages",
    "get_request_messages",
    "get_message_history",
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
    "get_history",
    "get_request_history",
    "get_latest_history",
    "count_history",
    "add_transfer_history",
    "add_status_history",
    "add_assignment_history",
    "add_admin_history",
    "add_expert_history",
    "delete_history",

    # holidays
    "add_holiday",
    "remove_holiday",
    "is_holiday",
    "get_holidays",

    # settings
    "get_setting",
    "set_setting",
    "delete_setting",
    "setting_exists",
    "get_all_settings",

    # tracking
    "generate_tracking_code",
    "get_next_tracking_number",

    # dashboard
    "get_dashboard",
    "get_dashboard_statistics",
    "get_dashboard_summary",
    "get_service_statistics",
    "get_daily_chart_data",
    "get_expert_statistics",
    "get_recent_activity",
    "get_sla_dashboard",

    # reports
    "normalize_statistics",
    "get_daily_statistics",
    "get_weekly_statistics",
    "get_monthly_statistics",
    "get_dashboard_report",
    "get_reports",
]
