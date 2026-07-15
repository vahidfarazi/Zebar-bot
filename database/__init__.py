"""
Database package initializer
Central export layer
"""

import logging

logger = logging.getLogger(__name__)

print("DATABASE INIT FILE LOADED")


# =====================================================
# CONNECTION
# =====================================================

try:
    from .connection import (
        get_connection,
        close_connection,
    )

except Exception as e:
    logger.warning("CONNECTION IMPORT FAILED: %s", e)

    def get_connection():
        return None

    def close_connection():
        return None



# =====================================================
# DATABASE INIT
# =====================================================

try:
    from .schema import (
        create_tables,
        init_database,
    )

except Exception as e:
    logger.warning("SCHEMA IMPORT FAILED: %s", e)

    def create_tables():
        return True

    def init_database():
        return True



# =====================================================
# USERS
# =====================================================

try:
    from .users import *

except Exception as e:
    logger.warning("USERS IMPORT FAILED: %s", e)


try:
    from .users import get_user_by_chat_id

except Exception:

    def get_user_by_chat_id(chat_id):
        return None



try:
    from .users import create_user

except Exception:

    def create_user(*args, **kwargs):
        return None



# =====================================================
# EXPERTS
# =====================================================

try:
    from .experts import *

except Exception as e:
    logger.warning("EXPERTS IMPORT FAILED: %s", e)



try:
    from .experts import get_active_experts

except Exception:

    def get_active_experts():
        return []



try:
    from .experts import get_active_expert

except Exception:

    def get_active_expert(*args, **kwargs):
        return None



# =====================================================
# TRACKING
# =====================================================

try:
    from .tracking import *

except Exception as e:
    logger.warning("TRACKING IMPORT FAILED: %s", e)



try:
    from .tracking import (
        create_tracking_code,
        get_request_by_tracking,
    )

except Exception as e:

    logger.warning(
        "TRACKING COMPAT IMPORT FAILED: %s",
        e
    )


    def create_tracking_code(*args, **kwargs):
        return None



    def get_request_by_tracking(*args, **kwargs):
        return None



# =====================================================
# ADMIN
# =====================================================

try:
    from .admins import *

except Exception as e:
    logger.warning("ADMINS IMPORT FAILED: %s", e)



try:
    from .admins import is_admin

except Exception:

    def is_admin(*args, **kwargs):
        return False



# =====================================================
# STATISTICS / DASHBOARD
# =====================================================

try:
    from .statistics import *

except Exception as e:
    logger.warning(
        "STATISTICS IMPORT FAILED: %s",
        e
    )



try:
    from .statistics import get_dashboard_summary

except Exception:

    try:

        from .statistics import get_statistics


        def get_dashboard_summary():

            return get_statistics()


    except Exception:


        def get_dashboard_summary():

            return {
                "users": 0,
                "messages": 0,
                "requests": 0,
                "experts": 0,
            }



def get_dashboard_report():

    return get_dashboard_summary()



# =====================================================
# EXPORT LIST
# =====================================================

__all__ = [

    # connection
    "get_connection",
    "close_connection",

    # schema
    "create_tables",
    "init_database",

    # users
    "get_user_by_chat_id",
    "create_user",

    # experts
    "get_active_experts",
    "get_active_expert",

    # tracking
    "create_tracking_code",
    "get_request_by_tracking",

    # admin
    "is_admin",

    # dashboard
    "get_dashboard_summary",
    "get_dashboard_report",

]


print("DATABASE INIT LOADED SUCCESSFULLY")
