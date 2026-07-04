"""
working_hours.py

All time-based rules for Azarakhsh system.
No handler should use datetime directly.
"""

from datetime import datetime, time
from config import Config
from database import is_holiday as db_is_holiday


# -----------------------------
# Current Time (Central Source)
# -----------------------------
def get_current_time() -> datetime:
    return datetime.now()


def get_current_date() -> str:
    return datetime.now().date().isoformat()


# -----------------------------
# Working Hours Config
# -----------------------------
def _parse_time(value: str) -> time:
    """
    Convert HH:MM string to time object.
    """
    hour, minute = map(int, value.split(":"))
    return time(hour=hour, minute=minute)


# -----------------------------
# Check Working Time
# -----------------------------
def is_working_time() -> bool:
    """
    Check if current time is within working hours.
    """

    current = get_current_time().time()

    start = _parse_time(Config.get("WORK_START", "07:00"))
    end = _parse_time(Config.get("WORK_END", "13:00"))

    return start <= current <= end


# -----------------------------
# Check Holiday
# -----------------------------
def is_holiday() -> bool:
    """
    Check if today is holiday.
    """
    today = get_current_date()
    return db_is_holiday(today)


# -----------------------------
# System Mode Check
# -----------------------------
def _system_mode() -> str:
    return Config.get("SYSTEM_MODE", "NORMAL")


# -----------------------------
# Can Create Request
# -----------------------------
def can_create_request() -> bool:
    """
    Determine if user can create request.
    """

    if _system_mode() == "DISABLED":
        return False

    if is_holiday():
        return False

    if not is_working_time():
        return False

    return True


# -----------------------------
# SLA Calculation (basic MVP)
# -----------------------------
def calculate_sla(start_time: datetime, end_time: datetime) -> int:
    """
    SLA in minutes (basic version).
    """

    delta = end_time - start_time
    return int(delta.total_seconds() / 60)


# -----------------------------
# Working Hours Info
# -----------------------------
def get_working_hours() -> dict:
    return {
        "start": Config.get("WORK_START", "07:00"),
        "end": Config.get("WORK_END", "13:00"),
    }
