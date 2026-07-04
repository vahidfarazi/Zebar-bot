"""
working_hours.py

Central time & SLA management for Azarakhsh system.
All time-based decisions must go through this module.
"""

from datetime import datetime, time
from config import Config


# -----------------------------
# Get current time (Asia/Tehran)
# -----------------------------
def get_current_time() -> datetime:
    """
    Return current system time.
    MVP: system time (later: timezone-safe version)
    """
    return datetime.now()


# -----------------------------
# Get current date
# -----------------------------
def get_current_date() -> str:
    """
    Return current date as ISO string.
    """
    return datetime.now().date().isoformat()


# -----------------------------
# Working hours check
# -----------------------------
def is_working_time() -> bool:
    """
    Check if current time is within working hours.
    """

    current = datetime.now().time()

    start_str = Config.get("WORK_START", "07:00")
    end_str = Config.get("WORK_END", "13:00")

    start_hour, start_min = map(int, start_str.split(":"))
    end_hour, end_min = map(int, end_str.split(":"))

    start_time = time(start_hour, start_min)
    end_time = time(end_hour, end_min)

    return start_time <= current <= end_time


# -----------------------------
# Holiday check
# -----------------------------
def is_holiday(date_str: str = None) -> bool:
    """
    Check if today is holiday.
    MVP: simple static check (DB version later)
    """

    if date_str is None:
        date_str = get_current_date()

    # MVP: placeholder (real version will query DB)
    # Example logic: Config-based or cached holidays
    holidays = Config.get("HOLIDAYS", "")

    if not holidays:
        return False

    holiday_list = [h.strip() for h in holidays.split(",")]

    return date_str in holiday_list


# -----------------------------
# Can create request
# -----------------------------
def can_create_request() -> bool:
    """
    Determine if request creation is allowed.
    """

    system_mode = Config.get("SYSTEM_MODE", "NORMAL")

    if system_mode != "NORMAL":
        return False

    if is_holiday():
        return False

    if not is_working_time():
        return False

    return True


# -----------------------------
# SLA calculation (MVP simple version)
# -----------------------------
def calculate_sla(start_time: datetime, end_time: datetime) -> int:
    """
    Calculate SLA in minutes.
    """

    delta = end_time - start_time
    return int(delta.total_seconds() / 60)
