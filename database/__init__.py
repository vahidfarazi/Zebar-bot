print("DATABASE INIT FILE LOADED")

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

try:
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

except ImportError as e:
    print("SETTINGS IMPORT WARNING:", e)



# -------------------------------------------------
# Requests
# -------------------------------------------------

try:
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

except ImportError as e:
    print("REQUESTS IMPORT WARNING:", e)



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

except ImportError as e:
    print("USERS IMPORT WARNING:", e)



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

except ImportError as e:
    print("EXPERTS IMPORT WARNING:", e)



# -------------------------------------------------
# Messages
# -------------------------------------------------

try:
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

except ImportError as e:
    print("MESSAGES IMPORT WARNING:", e)



# -------------------------------------------------
# History
# -------------------------------------------------

try:
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

except ImportError as e:
    print("HISTORY IMPORT WARNING:", e)



# -------------------------------------------------
# Holidays
# -------------------------------------------------

try:
    from .holidays import (
        add_holiday,
        remove_holiday,
        enable_holiday,
        disable_holiday,
        is_holiday,
        get_all_holidays,
        get_holidays,
    )

except ImportError as e:
    print("HOLIDAYS IMPORT WARNING:", e)



# -------------------------------------------------
# Admins
# -------------------------------------------------

try:
    from .admins import (
        is_admin,
        add_admin,
        remove_admin,
        get_all_admins,
        count_admins,
        admin_exists,
    )

except ImportError as e:
    print("ADMINS IMPORT WARNING:", e)



# -------------------------------------------------
# Tracking
# -------------------------------------------------

try:
    from .tracking import (
        create_tracking_code,
        get_tracking,
        add_tracking,
        update_tracking,
    )

except ImportError as e:
    print("TRACKING IMPORT WARNING:", e)



# -------------------------------------------------
# Statistics
# -------------------------------------------------

try:
    from .statistics import (
        get_statistics,
    )

except ImportError as e:
    print("STATISTICS IMPORT WARNING:", e)



# -------------------------------------------------
# Dashboard
# -------------------------------------------------

try:
    from .dashboard import (
        get_dashboard,
        get_dashboard_statistics,
        get_dashboard_summary,
        get_service_statistics,
        get_expert_statistics,
        get_recent_activity,
        get_sla_dashboard,
        get_daily_chart_data,
    )

except ImportError as e:
    print("DASHBOARD IMPORT WARNING:", e)



# -------------------------------------------------
# Reports
# -------------------------------------------------

try:
    from .reports import (
        get_daily_statistics,
        get_weekly_statistics,
        get_monthly_statistics,
        get_dashboard_report,
    )

except ImportError as e:
    print("REPORTS IMPORT WARNING:", e)



# -------------------------------------------------
# Schema
# -------------------------------------------------

try:
    from .schema import (
        create_tables,
    )

except ImportError as e:
    print("SCHEMA IMPORT WARNING:", e)



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
