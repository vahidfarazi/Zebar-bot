from datetime import datetime

from database import (
    get_setting,
    is_holiday
)


SYSTEM_NORMAL = "NORMAL"
SYSTEM_MAINTENANCE = "MAINTENANCE"
SYSTEM_CLOSED = "CLOSED"


def get_system_mode():

    mode = get_setting("system_mode")

    if mode is None:
        return SYSTEM_NORMAL

    return mode


def get_work_start():

    value = get_setting("work_start")

    if value is None:
        return 7

    return int(value)


def get_work_end():

    value = get_setting("work_end")

    if value is None:
        return 13

    return int(value)


def allow_new_request():

    value = get_setting("allow_new_request")

    if value is None:
        return True

    return value == "1"


def allow_status():

    value = get_setting("allow_status")

    if value is None:
        return True

    return value == "1"


def is_work_time():

    now = datetime.now()

    # جمعه
    if now.weekday() == 4:
        return False

    # تعطیلات ثبت شده
    if is_holiday(now.strftime("%Y-%m-%d")):
        return False

    start = get_work_start()
    end = get_work_end()

    return start <= now.hour < end


def get_system_status():

    mode = get_system_mode()

    if mode == SYSTEM_MAINTENANCE:
        return "MAINTENANCE"

    if mode == SYSTEM_CLOSED:
        return "CLOSED"

    if is_work_time():
        return "NORMAL"

    return "OUT_OF_TIME"
