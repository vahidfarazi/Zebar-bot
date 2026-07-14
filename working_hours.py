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
# Current Time
# ----------------------------------
def get_current_time() -> datetime:
    return datetime.now()


# ----------------------------------
# Current Date
# ----------------------------------
def get_current_date() -> str:
    return get_current_time().date().isoformat()


# ----------------------------------
# Parse Time
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
# Working Hours
# ----------------------------------
def get_work_start() -> str:

    return (
        get_setting(
            "WORK_START"
        )
        or "07:00"
    )


def get_work_end() -> str:

    return (
        get_setting(
            "WORK_END"
        )
        or "13:00"
    )


# ----------------------------------
# Working Days
# ----------------------------------
def get_working_days() -> list[int]:

    """
    Python weekday:
    Monday = 0
    Sunday = 6
    """

    value = (
        get_setting(
            "WORKING_DAYS"
        )
        or "0,1,2,3,4"
    )

    return [
        int(x)
        for x in value.split(",")
    ]


# ----------------------------------
# Check Working Day
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
# Check Holiday
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
# Check Working Time
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
# Full Working Status
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
# Can Create Request
# ----------------------------------
def can_create_request() -> bool:

    return (
        get_work_status()
        == "WORKING"
    )


# ----------------------------------
# Can Track Request
# ----------------------------------
def can_track_request() -> bool:

    return True


# ----------------------------------
# User Message
# ----------------------------------
def availability_message() -> str:

    status = get_work_status()


    if status == "HOLIDAY":

        return (
            "📅 امروز تعطیل رسمی است.\n\n"
            "در حال حاضر فقط امکان پیگیری درخواست‌ها وجود دارد."
        )


    if status == "WEEKEND":

        return (
            "📅 امروز خارج از روزهای کاری است.\n\n"
            "در حال حاضر فقط امکان پیگیری درخواست‌ها وجود دارد."
        )


    if status == "OUTSIDE":

        return (
            "⏰ در حال حاضر خارج از ساعت کاری هستیم.\n\n"
            "ساعات پاسخگویی:\n"
            f"🕖 {get_work_start()} تا {get_work_end()}\n\n"
            "در این زمان فقط امکان پیگیری درخواست وجود دارد."
        )


    return (
        "🟢 سامانه آماده ثبت درخواست است."
    )


# ----------------------------------
# SLA Calculator
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
