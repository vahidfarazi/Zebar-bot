"""
tracking.py

Tracking code generator and validator.

Format:
SR-YYYY-0000001
"""

import re
from datetime import datetime
from typing import Optional

from database import fetch_one, execute
from validators import validate_tracking


TRACKING_REGEX = r"^SR-[0-9]{4}-[0-9]{7}$"


# -----------------------------
# Get Current Persian Year (Simple version)
# -----------------------------
def get_current_year() -> int:
    """
    Return current year (approximation).
    In production, should use Jalali calendar.
    """
    return datetime.now().year + 621


# -----------------------------
# Get Last Tracking Number
# -----------------------------
def _get_last_sequence(year: int) -> int:
    """
    Fetch last sequence number for given year.
    """

    row = fetch_one("""
        SELECT tracking_code
        FROM requests
        WHERE tracking_code LIKE ?
        ORDER BY id DESC
        LIMIT 1
    """, (f"SR-{year}-%",))

    if not row or not row["tracking_code"]:
        return 0

    try:
        return int(row["tracking_code"].split("-")[-1])
    except Exception:
        return 0


# -----------------------------
# Generate Tracking Code
# -----------------------------
def generate_tracking_code() -> str:
    """
    Generate unique tracking code.
    """

    year = get_current_year()
    last_seq = _get_last_sequence(year)

    new_seq = last_seq + 1
    seq_str = str(new_seq).zfill(7)

    tracking_code = f"SR-{year}-{seq_str}"

    return tracking_code


# -----------------------------
# Save Tracking (optional helper)
# -----------------------------
def save_tracking_for_request(request_id: int, tracking_code: str) -> None:
    """
    Assign tracking code to request.
    """

    execute("""
        UPDATE requests
        SET tracking_code = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (tracking_code, request_id))


# -----------------------------
# Validate Tracking Code
# -----------------------------
def validate_tracking_code(code: str) -> bool:
    """
    Validate tracking format + regex.
    """
    if not isinstance(code, str):
        return False

    return re.match(TRACKING_REGEX, code) is not None


# -----------------------------
# Safe Wrapper
# -----------------------------
def generate_and_save_tracking(request_id: int) -> str:
    """
    Generate tracking and persist it.
    """

    tracking_code = generate_tracking_code()
    save_tracking_for_request(request_id, tracking_code)

    return tracking_code
