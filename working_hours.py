"""
working_hours.py

Responsible for all time-based rules:
- working hours check
- holiday check
- SLA calculation
- request creation permission
"""

from datetime import datetime, time
from typing import Optional

from config import Config
from database import fetch_all
from logger import log_warning


# -----------------------------
# Timezone (fixed)
# -----------------------------
TIMEZONE = "Asia/Tehran"


# -----------------------------
# Helpers
# -----------------------------
def get_current_time() -> datetime:
    """
    Return current server time.
    (Timezone handling can be improved in future versions)
    """
    return datetime.now()


def get_current_date() -> str:
    """
    Return current date in YYYY-MM-DD format.
    """
    return get_current_time().strftime("%Y-%m-%d")


# -----------------------------
# Working Hours
# -----------------------------
def _parse_time(value: str) -> time:
    """
    Convert HH:MM string to time object.
    """
    hour, minute = value.split(":")
    return time(int(hour), int(minute))


def get_working_hours() -> tuple[time, time]:
    """
    Read working hours from config.
    """
    start = Config.get("WORK_START", "07:00")
    end = Config.get("WORK_END", "13:00")
    return _parse_time(start), _parse_time(end)


def is_working_time() -> bool:
    """
    Check if current time is inside working hours.
    """
    now = get_current_time().time()
    start, end = get_working_hours()
    return start <= now <= end


# -----------------------------
# Holidays
# -----------------------------
def is_holiday() -> bool:
    """
    Check if today is a holiday.
    """
    today = get_current_date()

    holidays = fetch_all(
        "SELECT holiday_date FROM holidays WHERE enabled = 1"
    )

    holiday_dates = {h["holiday_date"] for h in holidays}
    return today in holiday_dates


# -----------------------------
# System Mode Check
# -----------------------------
def _get_system_mode() -> str:
    return Config.get("SYSTEM_MODE", "NORMAL")


# -----------------------------
# Request Permission
# -----------------------------
def can_create_request() -> bool:
    """
    Determine if request creation is allowed.
    """

    system_mode = _get_system_mode()

    if system_mode == "DISABLED":
        return False

    if system_mode == "MAINTENANCE":
        return False

    if is_holiday():
        return False

    if not is_working_time():
        return False

    return True


# -----------------------------
# SLA Calculation (simple version)
# -----------------------------
def calculate_sla(created_at: datetime, closed_at: Optional[datetime]) -> Optional[int]:
    """
    Return SLA in minutes (simple implementation).
    """

    if not closed_at:
        return None

    try:
        delta = closed_at - created_at
        return int(delta.total_seconds() / 60)
    except Exception as e:
        log_warning(
            "working_hours",
            "sla_error",
            str(e),
        )
        return None
