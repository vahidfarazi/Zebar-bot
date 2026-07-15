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
    from .settings import *

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
    from .users import *

except Exception as e:
    print("USERS IMPORT WARNING:", e)



# =================================================
# EXPERTS
# =================================================

try:
    from .experts import *

except Exception as e:
    print("EXPERTS IMPORT WARNING:", e)



# =================================================
# MESSAGES
# =================================================

try:
    from .messages import *

except Exception as e:
    print("MESSAGES IMPORT WARNING:", e)



# =================================================
# HISTORY
# =================================================

try:
    from .history import *

except Exception as e:
    print("HISTORY IMPORT WARNING:", e)



# =================================================
# TRACKING
# =================================================

try:
    from .tracking import *

except Exception as e:
    print("TRACKING IMPORT WARNING:", e)



# =================================================
# HOLIDAYS
# =================================================

try:
    from .holidays import *

except Exception as e:
    print("HOLIDAYS IMPORT WARNING:", e)



# =================================================
# ADMINS
# =================================================

try:
    from .admins import *

except Exception as e:
    print("ADMINS IMPORT WARNING:", e)



# =================================================
# STATISTICS
# =================================================

try:
    from .statistics import *

except Exception as e:
    print("STATISTICS IMPORT WARNING:", e)



# =================================================
# SCHEMA
# =================================================

try:
    from .schema import *

except Exception as e:
    print("SCHEMA IMPORT WARNING:", e)



# =================================================
# DASHBOARD COMPATIBILITY
# =================================================

try:

    from .statistics import get_dashboard_summary


    # backward compatibility
    get_dashboard_report = get_dashboard_summary


except Exception as e:

    print(
        "DASHBOARD IMPORT WARNING:",
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


print(
    "DATABASE INIT LOADED SUCCESSFULLY"
)
