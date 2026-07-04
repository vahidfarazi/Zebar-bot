"""
tracking.py

Responsible for generating and validating tracking codes.
Format: SR-YYYY-0000001
"""

import re
from datetime import datetime
from database import fetch_one, execute


TRACKING_REGEX = r"^SR-[0-9]{4}-[0-9]{7}$"


# -----------------------------
# Current Year (Persian/Tehran logic simplified placeholder)
# -----------------------------
def _get_current_year() -> str:
    return datetime.now().strftime("%Y")


# -----------------------------
# Generate Tracking Code
# -----------------------------
def generate_tracking_code() -> str:
    """
    Generate unique tracking code based on last record in DB.
    """

    year = _get_current_year()

    result = fetch_one(
        """
        SELECT tracking_code
        FROM requests
        WHERE tracking_code LIKE ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (f"SR-{year}-%",),
    )

    if result and result["tracking_code"]:
        last_code = result["tracking_code"]
        last_number = int(last_code.split("-")[-1])
        next_number = last_number + 1
    else:
        next_number = 1

    tracking_code = f"SR-{year}-{next_number:07d}"
    return tracking_code


# -----------------------------
# Validate Tracking Code
# -----------------------------
def validate_tracking_code(code: str) -> bool:
    """
    Validate tracking format using regex.
    """
    return re.match(TRACKING_REGEX, code) is not None


# -----------------------------
# Save Tracking (optional helper)
# -----------------------------
def save_tracking(request_id: int, tracking_code: str) -> None:
    """
    Attach tracking code to request.
    """
    execute(
        """
        UPDATE requests
        SET tracking_code = ?
        WHERE id = ?
        """,
        (tracking_code, request_id),
    )
