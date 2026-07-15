"""
database/__init__.py

Database package exports.
"""

# Database initialization
from .schema import init_database


# CRUD
from .crud import (
    execute,
    fetch_one,
    fetch_all,
    execute_many,
    table_exists,
)


# Connection
from .connection import get_connection


# Users
from .users import (
    create_user,
    get_user,
    update_username,
    update_full_name,
    update_role,
    get_all_users,
)


# Admins
from .admins import (
    add_admin,
    remove_admin,
    is_admin,
    admin_exists,
    get_all_admins,
    count_admins,
)


# Experts
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


# Messages
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


# History
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


# Tracking
from .tracking import (
    get_last_tracking_number,
)


from .tracking_sequence import (
    get_next_tracking_number,
)


# Holidays
from .holidays import (
    add_holiday,
    remove_holiday,
    enable_holiday,
    disable_holiday,
    is_holiday,
    get_all_holidays,
    get_holidays,
)


# Logs
from .logs import (
    insert_log,
    get_logs,
    clear_logs,
)


# Reports
from .reports import (
    get_daily_statistics,
    get_weekly_statistics,
    get_monthly_statistics,
    get_daily_chart_data,
    get_service_statistics,
    get_expert_statistics,
    get_dashboard_report,
)


# Dashboard
from .dashboard import (
    get_dashboard_statistics,
    get_dashboard,
)


# -------------------------------------------------
# Settings
# -------------------------------------------------

from .settings import (
    get_setting,
    set_setting,
    delete_setting,
    get_all_settings,
)


__all__ = [

    # init
    "init_database",

    # connection
    "get_connection",

    # crud
    "execute",
    "fetch_one",
    "fetch_all",
    "execute_many",
    "table_exists",

    # settings
    "get_setting",
    "set_setting",
    "delete_setting",
    "get_all_settings",

]
