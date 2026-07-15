print("DATABASE INIT FILE LOADED")


"""
database package

Central database exports.
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
# SETTINGS
# =================================================

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
except Exception as e:
    print("SETTINGS IMPORT WARNING:", e)



# =================================================
# REQUESTS
# =================================================

try:
    from .requests import *

except Exception as e:
    print("REQUESTS IMPORT WARNING:", e)



# =================================================
# USERS
# =================================================

try:

    from .users import (

        create_user,

        get_user,

        get_user_by_chat_id,

        update_user,

        delete_user,

    )

except Exception as e:

    print(
        "USERS IMPORT WARNING:",
        e
    )



# =================================================
# EXPERTS
# =================================================

try:

    from .experts import (

        create_expert,

        get_expert,

        get_active_experts,

        update_expert,

    )

except Exception as e:

    print(
        "EXPERTS IMPORT WARNING:",
        e
    )



# =================================================
# MESSAGES
# =================================================

try:

    from .messages import *

except Exception as e:

    print(
        "MESSAGES IMPORT WARNING:",
        e
    )



# =================================================
# HISTORY
# =================================================

try:

    from .history import *

except Exception as e:

    print(
        "HISTORY IMPORT WARNING:",
        e
    )



# =================================================
# TRACKING
# =================================================

try:

    from .tracking import (

        create_tracking_code,

    )

except Exception as e:

    print(
        "TRACKING IMPORT WARNING:",
        e
    )



# =================================================
# HOLIDAYS
# =================================================

try:

    from .holidays import *

except Exception as e:

    print(
        "HOLIDAYS IMPORT WARNING:",
        e
    )



# =================================================
# ADMINS
# =================================================

try:

    from .admins import (

        is_admin,

        add_admin,

        remove_admin,

        get_all_admins,

        count_admins,

        admin_exists,

        set_active,

        get_active,

        get_dashboard_summary,

    )


except Exception as e:

    print(
        "ADMINS IMPORT WARNING:",
        e
    )



# =================================================
# STATISTICS
# =================================================

try:

    from .statistics import (

        get_statistics,

    )

except Exception as e:

    print(
        "STATISTICS IMPORT WARNING:",
        e
    )



# =================================================
# SCHEMA
# =================================================

try:

    from .schema import (

        create_tables,

    )


except Exception as e:

    print(
        "SCHEMA IMPORT WARNING:",
        e
    )



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
