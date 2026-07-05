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
    get_expert,
    list_active_experts,
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
    "get_connection",
    "init_database",
    "execute",
    "fetch_one",
    "fetch_all",
    "get_setting",
    "set_setting",
    "insert_request",
    "get_request_by_tracking",
    "update_request_status",
    "get_last_tracking_number",
    "get_user",
    "create_user",
    "get_expert",
    "list_active_experts",
    "is_admin",
    "is_holiday",
    "insert_log",
]
