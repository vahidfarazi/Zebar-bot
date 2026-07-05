"""
tracking_service.py

Tracking number generation service.
"""

from datetime import datetime

from database import get_last_tracking_number


def generate_tracking_code() -> str:
    """
    Generate next tracking code.

    Format:
    SR-YYYY-0000001
    """

    year = datetime.now().year

    last_number = get_last_tracking_number(year)

    next_number = last_number + 1

    return f"SR-{year}-{next_number:07d}"
