from datetime import datetime

from core.settings import (
    SYSTEM_MODE,
    WORK_START,
    WORK_END,
    HOLIDAYS
)


def is_friday():

    # Monday=0 ... Friday=4 ... Sunday=6
    return datetime.now().weekday() == 4


def is_work_time():

    now = datetime.now()

    return WORK_START <= now.hour < WORK_END


def is_holiday():

    today = datetime.now().strftime("%Y-%m-%d")

    return today in HOLIDAYS


def get_system_status():

    if SYSTEM_MODE == "MAINTENANCE":
        return "MAINTENANCE"

    if SYSTEM_MODE == "CLOSED":
        return "CLOSED"

    if is_holiday():
        return "HOLIDAY"

    if is_friday():
        return "HOLIDAY"

    if is_work_time():
        return "WORK_TIME"

    return "OUT_OF_TIME"
