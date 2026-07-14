"""
working_hours.py

Central working hours and request availability manager.
"""

from datetime import datetime, time

from database import (
    is_holiday as db_is_holiday,
    get_setting,
)


# ----------------------------------
# Current
# ----------------------------------

def get_current_time() -> datetime:
    return datetime.now()


def get_current_date() -> str:
    return get_current_time().date().isoformat()


# ----------------------------------
# Time Parser
# ----------------------------------

def parse_time(value: str) -> time:

    hour, minute = map(
        int,
        value.split(":"),
    )

    return time(
        hour,
        minute,
    )


# ----------------------------------
# Settings
# ----------------------------------

def get_work_start() -> str:

    return (
        get_setting("WORK_START")
        or "07:00"
    )


def get_work_end() -> str:

    return (
        get_setting("WORK_END")
        or "13:00"
    )


def get_working_days() -> list[int]:

    """
    Iran working days:

    Saturday = 5
    Sunday = 6
    Monday = 0
    Tuesday = 1
    Wednesday = 2
    Thursday = 3

    Friday = 4 holiday
    """

    value = (
        get_setting("WORKING_DAYS")
        or "5,6,0,1,2,3"
    )

    return [
        int(x)
        for x in value.split(",")
    ]


# ----------------------------------
# Working Day
# ----------------------------------

def is_working_day(
    date=None,
) -> bool:

    if date is None:

        date = get_current_time()


    return (
        date.weekday()
        in get_working_days()
    )


# ----------------------------------
# Holiday
# ----------------------------------

def is_holiday(
    date_str: str | None = None,
) -> bool:


    if date_str is None:

        date_str = get_current_date()


    return db_is_holiday(
        date_str
    )


# ----------------------------------
# Working Time
# ----------------------------------

def is_working_time() -> bool:


    now = (
        get_current_time()
        .time()
    )


    start = parse_time(
        get_work_start()
    )


    end = parse_time(
        get_work_end()
    )


    return (
        start <= now <= end
    )


# ----------------------------------
# System Status
# ----------------------------------

def get_work_status() -> str:


    if is_holiday():

        return "HOLIDAY"


    if not is_working_day():

        return "WEEKEND"


    if not is_working_time():

        return "OUTSIDE"


    return "WORKING"



# ----------------------------------
# Permissions
# ----------------------------------

def can_create_request() -> bool:

    return (
        get_work_status()
        == "WORKING"
    )


def can_track_request() -> bool:

    return True



# ----------------------------------
# Dashboard Status
# ----------------------------------

def get_system_work_status() -> dict:


    status = get_work_status()


    mapping = {

        "WORKING":
            "🟢 فعال",

        "OUTSIDE":
            "🟡 خارج ساعت کاری",

        "HOLIDAY":
            "🔴 تعطیل رسمی",

        "WEEKEND":
            "🔴 روز غیرکاری",

    }


    return {

        "status": status,

        "title":
            mapping.get(
                status,
                status,
            ),

        "start":
            get_work_start(),

        "end":
            get_work_end(),

        "can_create":
            can_create_request(),

    }



# ----------------------------------
# User Message
# ----------------------------------

def availability_message() -> str:


    status = get_work_status()



    if status == "HOLIDAY":

        return (
            "📅 امروز تعطیل رسمی است.\n\n"
            "در حال حاضر فقط امکان پیگیری درخواست وجود دارد."
        )


    if status == "WEEKEND":

        return (
            "📅 امروز روز کاری نیست.\n\n"
            "در حال حاضر فقط امکان پیگیری درخواست وجود دارد."
        )


    if status == "OUTSIDE":

        return (
            "⏰ خارج از ساعت کاری هستیم.\n\n"
            f"🕖 ساعات کاری: "
            f"{get_work_start()} تا {get_work_end()}\n\n"
            "فقط امکان پیگیری درخواست وجود دارد."
        )


    return (
        "🟢 سامانه آماده ثبت درخواست است."
    )



# ----------------------------------
# SLA
# ----------------------------------

def calculate_sla(
    start_time: datetime,
    end_time: datetime,
) -> int:


    return int(
        (
            end_time - start_time
        )
        .total_seconds()
        // 60
    )
