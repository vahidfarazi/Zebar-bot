"""
database

Central database package for Azarakhsh.
Exports all public database functions.
"""

# Connection
from .connection import get_connection

# Schema
from .schema import init_database

# Generic CRUD
from .crud import (
    execute,
    execute_many,
    fetch_one,
    fetch_all,
    table_exists,
)

# Settings
from .settings import (
    get_setting,
    set_setting,
)

# Requests
from .requests import (
    insert_request,
    get_request,
    get_request_by_tracking,
    get_user_requests,
    update_request_status,
    assign_expert,
    save_expert_message,
    close_request,
    update_priority,
    delete_request,

    get_dashboard_statistics,
    get_recent_requests,
)

# Request Messages
from .messages import (
    add_message,
    get_message,
    get_messages,
    get_last_message,
    delete_messages,
)

# Request History
from .history import (
    add_history,
    get_history,
    delete_history,
)

# Tracking
from .tracking import (
    get_last_tracking_number,
)

from .tracking_sequence import (
    get_next_tracking_number,
)

# Users
from .users import (
    get_user,
    create_user,
)

# Experts
from .experts import (
    create_expert,
    get_expert,
    list_active_experts,
    update_department,
    set_active,
    delete_expert,
)

# Admins
from .admins import (
    is_admin,
)

# Holidays
from .holidays import (
    is_holiday,
    add_holiday,
    remove_holiday,
)

# Logs
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
    "save_expert_message",
    "close_request",
    "update_priority",
    "delete_request",

    "get_dashboard_statistics",
    "get_recent_requests",
        # Messages
    "add_message",
    "get_message",
    "get_messages",
    "get_last_message",
    "delete_messages",

    # History
    "add_history",
    "get_history",
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
    "list_active_experts",
    "update_department",
    "set_active",
    "delete_expert",

    # Admins
    "is_admin",

    # Holidays
    "is_holiday",
    "add_holiday",
    "remove_holiday",

    # Logs
    "insert_log",
]
