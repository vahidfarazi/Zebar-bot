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
    get_messages,
    get_last_message,
)


# =====================================================
# HISTORY
# =====================================================

from .history import (
    add_history,
    get_history,
)


# =====================================================
# SETTINGS
# =====================================================

from .settings import (
    get_setting,
    set_setting,
    delete_setting,
    get_all_settings,
)


# =====================================================
# HOLIDAYS
# =====================================================

from .holidays import (
    add_holiday,
    remove_holiday,
    get_holidays,
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
# DASHBOARD
# =====================================================

from .dashboard import (
    get_dashboard_statistics,
    get_dashboard,
    get_dashboard_summary,
)



def get_dashboard_report():

    return get_dashboard()



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
    "close_request",

    # tracking
    "create_tracking_code",
    "get_last_tracking_number",

    # settings
    "get_setting",
    "set_setting",

    # dashboard
    "get_dashboard",
    "get_dashboard_report",

]
