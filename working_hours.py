"""
working_hours.py

Handles all time-based logic:
- working hours
- holidays
- system availability
- SLA calculation (future)
"""

from datetime import datetime, time
from typing import Optional

from config import Config
from database import fetch_one, fetch_all
from logger import log_warning


# -----------------------------
# Time Helpers
# -----------------------------
def get_current_time() -> datetime:
    """
    Return current system time.
    """
    return datetime.now()


def get_current_date() -> str:
    """
    Return current date in YYYY-MM-DD.
    """
    return datetime.now().strftime("%Y-%m-%d")


# -----------------------------
# Working Hours
# -----------------------------
def _parse_time(value: str) -> time:
    """
    Convert HH:MM string to time object.
    """
    try:
        hour, minute = map(int, value.split(":"))
        return time(hour=hour, minute=minute)
    except Exception:
        log_warning("working_hours", "parse_error", "Invalid time format")
        return time(0, 0)


def get_working_hours() -> tuple[time, time]:
    """
    Get working hours from config.
    """
    start = Config.get("WORK_START", "07:00")
    end = Config.get("WORK_END", "13:00")

    return _parse_time(start), _parse_time(end)


def is_working_time() -> bool:
    """
    Check if current time is within working hours.
    """

    start_time, end_time = get_working_hours()
    now = datetime.now().time()

    # Handle normal range
    if start_time <= end_time:
        return start_time <= now <= end_time

    # Handle overnight range (future support)
    return now >= start_time or now <= end_time


# -----------------------------
# Holiday Check
# -----------------------------
def is_holiday() -> bool:
    """
    Check if today is holiday.
    """

    today = get_current_date()

    row = fetch_one("""
        SELECT holiday_date
        FROM holidays
        WHERE holiday_date = ? AND enabled = 1
    """, (today,))

    return row is not None


# -----------------------------
# System Mode Check
# -----------------------------
def get_system_mode() -> str:
    """
    Get system mode from config.
    """
    return Config.get("SYSTEM_MODE", "NORMAL")


def can_create_request() -> bool:
    """
    Check if user can create request.
    """

    mode = get_system_mode()

    if mode == "DISABLED":
        return False

    if mode == "MAINTENANCE":
        return False

    if is_holiday():
        return False

    if not is_working_time():
        return False

    return True


# -----------------------------
# SLA Calculation (Basic)
# -----------------------------
def calculate_sla(start_time: datetime, end_time: Optional[datetime] = None) -> int:
    """
    Calculate SLA in minutes (working hours only - simplified).
    """

    end_time = end_time or datetime.now()

    if end_time < start_time:
        return 0

    delta = end_time - start_time

    # Simple SLA (future: exclude non-working hours)
    return int(delta.total_seconds() / 60)


# -----------------------------
# Status Message Helpers (optional)
# -----------------------------
def get_working_status_message() -> Optional[str]:
    """
    Return system status message if not available.
    """

    mode = get_system_mode()

    if mode == "MAINTENANCE":
        return "MAINTENANCE_MODE"

    if mode == "DISABLED":
        return "OUT_OF_WORK_TIME"

    if is_holiday():
        return "HOLIDAY_MESSAGE"

    if not is_working_time():
        return "OUT_OF_WORK_TIME"

    return None
