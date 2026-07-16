"""
database/tracking.py

Tracking number repository.
"""

from datetime import datetime

from .crud import fetch_one


# =================================================
# Last Tracking Number
# =================================================

def get_last_tracking_number() -> str | None:
    """
    Return latest tracking code of current year.

    Format:
        SR-2026-0000001
    """

    year = datetime.now().year

    row = fetch_one(
        """
        SELECT tracking_code

        FROM requests

        WHERE tracking_code LIKE %s

        ORDER BY id DESC

        LIMIT 1
        """,
        (
            f"SR-{year}-%",
        ),
    )

    if not row:
        return None

    return row["tracking_code"]



# =================================================
# Current Year
# =================================================

def get_tracking_year() -> int:
    """
    Return current tracking year.
    """

    return datetime.now().year



# =================================================
# Exists
# =================================================

def tracking_exists(
    tracking_code: str,
) -> bool:
    """
    Check tracking code existence.
    """

    row = fetch_one(
        """
        SELECT tracking_code

        FROM requests

        WHERE tracking_code=%s

        LIMIT 1
        """,
        (
            tracking_code,
        ),
    )

    return row is not None



# =================================================
# Extract Sequence
# =================================================

def extract_tracking_sequence(
    tracking_code: str,
) -> int:

    try:

        return int(
            tracking_code.split("-")[-1]
        )

    except Exception:

        return 0



# =================================================
# Last Sequence
# =================================================

def get_last_sequence() -> int:
    """
    Return last numeric sequence.
    """

    code = get_last_tracking_number()

    if not code:
        return 0

    return extract_tracking_sequence(
        code
    )

# =================================================
# Next Tracking Number
# =================================================

def get_next_tracking_number() -> str:
    """
    Return next tracking code.

    Format:
        SR-2026-0000001
    """

    year = get_tracking_year()

    sequence = get_last_sequence() + 1

    return f"SR-{year}-{sequence:07d}"


# =================================================
# Generate Tracking Code
# =================================================

def generate_tracking_code() -> str:
    """
    Alias for compatibility.
    """

    return get_next_tracking_number()
