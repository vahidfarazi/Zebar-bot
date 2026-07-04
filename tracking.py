"""
tracking.py

Tracking system for Azarakhsh.
Format: SR-YYYY-0000001
"""

import re
from datetime import datetime

from database import get_last_tracking_number
from config import Config


TRACKING_REGEX = r"^SR-[0-9]{4}-[0-9]{7}$"


# -----------------------------
# Validate Tracking
# -----------------------------
def validate_tracking(tracking_code: str) -> bool:
    if not tracking_code:
        return False

    return bool(re.match(TRACKING_REGEX, tracking_code))


# -----------------------------
# Get Current Year (System Timezone)
# -----------------------------
def _get_year() -> int:
    """
    Year extraction (placeholder for Jalali future support).
    """
    return datetime.now().year


# -----------------------------
# Generate Tracking Code
# -----------------------------
def generate_tracking_code() -> str:
    """
    Generate unique tracking code.
    """

    year = _get_year()

    last_number = get_last_tracking_number(year)

    if last_number is None:
        next_number = 1
    else:
        next_number = last_number + 1

    return f"SR-{year}-{str(next_number).zfill(7)}"
