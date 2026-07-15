"""
database package

Central database exports.
"""

# -------------------------------------------------
# Initialize database
# -------------------------------------------------

from .connection import (
    get_connection,
    init_database,
)


# -------------------------------------------------
# CRUD
# -------------------------------------------------

from .crud import (
    execute,
    fetch_one,
    fetch_all,
)


# -------------------------------------------------
# Settings
# -------------------------------------------------

from .settings import (
    get_setting,
    set_setting,
    delete_setting,
    get_all_settings,
    get_working_hours,
    set_working_hours,
    get_bool_setting,
    set_bool_setting,
)


# -------------------------------------------------
# Requests
# -------------------------------------------------

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
    get_sla_statistics,
)


# -------------------------------------------------
# Users
# -------------------------------------------------

try:
    from .users import (
        create_user,
        get_user,
        get_user_by_chat_id,
        update_user,
        delete_user,
    )
except ImportError:
    pass


# -------------------------------------------------
# Experts
# -------------------------------------------------

try:
    from .experts import (
        create_expert,
        get_expert,
        get_active_experts,
        update_expert,
    )
except ImportError:
    pass


# -------------------------------------------------
# Messages
# -------------------------------------------------

try:
    from .messages import (
        save_message,
        get_messages,
    )
except ImportError:
    pass


# -------------------------------------------------
# Database Ready
# -------------------------------------------------

try:
    init_database()
    print("DATABASE INITIALIZED")
except Exception as e:
    print(
        "DATABASE INIT WARNING:",
        e,
    )
