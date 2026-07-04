"""
working_hours.py

Central time & SLA management for Azarakhsh system.
"""

from datetime import datetime, time

from config import Config
from database import is_holiday as db_is_holiday


# -----------------------------
# Current Time
# -----------------------------
def get_current_time() -> datetime:
    """
    Return current system datetime.
    """
    return datetime.now()


# -----------------------------
# Current Date
# -----------------------------
def get_current_date() -> str:
    """
    Return current date (YYYY-MM-DD).
    """
    return get_current_time().date().isoformat()


# -----------------------------
# Working Time
# -----------------------------
def is_working_time() -> bool:
    """
    Check whether current time is inside working hours.
    """

    now = get_current_time().time()

    start = Config.get_str("WORK_START", "07:00")
    end = Config.get_str("WORK_END", "13:00")

    start_hour, start_minute = map(int, start.split(":"))
    end_hour, end_minute = map(int, end.split(":"))

    start_time = time(start_hour, start_minute)
    end_time = time(end_hour, end_minute)

    return start_time <= now <= end_time


# -----------------------------
# Holiday
# -----------------------------
def is_holiday(date_str: str | None = None) -> bool:
    """
    Check whether the given date is a holiday.
    """

    if date_str is None:
        date_str = get_current_date()

    return db_is_holiday(date_str)


# -----------------------------
# Request Availability
# -----------------------------
def can_create_request() -> bool:
    """
    Determine whether creating a new request is currently allowed.
    """

    if not Config.get_bool("ALLOW_NEW_REQUEST", True):
        return False

    if Config.get_str("SYSTEM_MODE", "NORMAL") != "NORMAL":
        return False

    if is_holiday():
        return False

    if not is_working_time():
        return False

    return True


# -----------------------------
# SLA
# -----------------------------
def calculate_sla(
    start_time: datetime,
    end_time: datetime,
) -> int:
    """
    Calculate SLA duration in minutes.
    """

    return int(
        (end_time - start_time).total_seconds() // 60
    )
