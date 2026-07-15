print("DATABASE INIT FILE LOADED")

"""
database package
Central database exports
"""


# =================================================
# CONNECTION
# =================================================

from .connection import (
    get_connection,
    init_database,
)


# =================================================
# CRUD
# =================================================

from .crud import (
    execute,
    fetch_one,
    fetch_all,
)



# =================================================
# SAFE IMPORT HELPER
# =================================================

def _safe_import(module, names):

    result = {}

    try:
        mod = __import__(
            f"database.{module}",
            fromlist=names
        )

        for name in names:

            if hasattr(mod, name):
                result[name] = getattr(mod, name)

    except Exception as e:

        print(
            f"{module.upper()} IMPORT WARNING:",
            e
        )

    globals().update(result)



# =================================================
# LOAD MODULES
# =================================================


_safe_import(
    "settings",
    [
        "get_setting",
        "set_setting",
        "delete_setting",
        "get_all_settings",
        "get_working_hours",
        "set_working_hours",
        "get_bool_setting",
        "set_bool_setting",
    ]
)



_safe_import(
    "requests",
    [
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
        "get_sla_statistics",
    ]
)



_safe_import(
    "users",
    [
        "create_user",
        "get_user",
        "get_user_by_chat_id",
        "update_user",
        "delete_user",
    ]
)



_safe_import(
    "experts",
    [
        "create_expert",
        "get_expert",
        "get_active_experts",
        "update_expert",
    ]
)



_safe_import(
    "messages",
    [
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
    ]
)



_safe_import(
    "history",
    [
        "add_history",
        "get_latest_history",
        "count_history",
        "add_transfer_history",
        "add_status_history",
        "add_assignment_history",
        "add_admin_history",
        "add_expert_history",
        "delete_history",
    ]
)



_safe_import(
    "tracking",
    [
        "create_tracking_code",
    ]
)



_safe_import(
    "holidays",
    [
        "add_holiday",
        "remove_holiday",
        "enable_holiday",
        "disable_holiday",
        "is_holiday",
        "get_all_holidays",
        "get_holidays",
    ]
)



_safe_import(
    "admins",
    [
        "is_admin",
        "add_admin",
        "remove_admin",
        "get_all_admins",
        "count_admins",
        "admin_exists",
        "set_active",
        "get_active",
    ]
)



_safe_import(
    "statistics",
    [
        "get_statistics",
        "get_dashboard_summary",
    ]
)



_safe_import(
    "schema",
    [
        "create_tables",
    ]
)



# =================================================
# FALLBACKS
# =================================================

# جلوگیری از Crash اگر بعضی فایل‌ها هنوز ساخته نشده‌اند


if "get_dashboard_summary" not in globals():

    def get_dashboard_summary():

        return {
            "users": 0,
            "requests": 0,
            "experts": 0,
            "messages": 0,
        }



if "get_statistics" not in globals():

    def get_statistics():

        return {}



if "get_active" not in globals():

    def get_active():

        return []



if "set_active" not in globals():

    def set_active(*args, **kwargs):

        return None



if "create_tables" not in globals():

    def create_tables():

        return None



print("DATABASE INIT LOADED SUCCESSFULLY")



# =================================================
# DATABASE INIT
# =================================================

try:

    init_database()

    print(
        "DATABASE INITIALIZED"
    )

except Exception as e:

    print(
        "DATABASE INIT WARNING:",
        e
    )
