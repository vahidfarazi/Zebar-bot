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
    fetch_one,
    fetch_all,
    execute_many,
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
    get_request_by_tracking,
    update_request_status,
)

# Tracking
from .tracking import (
    get_last_tracking_number,
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
    "fetch_one",
    "fetch_all",
    "execute_many",
    "table_exists",

    # Settings
    "get_setting",
    "set_setting",

    # Requests
    "insert_request",
    "get_request_by_tracking",
    "update_request_status",

    # Tracking
    "get_last_tracking_number",

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

    # Logs
    "insert_log",
]
