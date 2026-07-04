"""
validators.py

Input validation layer for Azarakhsh system.

Rule:
- No DB access
- No business logic
- Only pure validation
"""

import re


# -----------------------------
# Tracking Code Validation
# -----------------------------
TRACKING_REGEX = r"^SR-[0-9]{4}-[0-9]{7}$"


def validate_tracking(code: str) -> bool:
    """
    Validate tracking code format.
    """
    if not isinstance(code, str):
        return False

    return re.match(TRACKING_REGEX, code) is not None


# -----------------------------
# Mobile Validation
# -----------------------------
MOBILE_REGEX = r"^09[0-9]{9}$"


def validate_mobile(mobile: str) -> bool:
    """
    Validate Iranian mobile number format.
    """
    if not isinstance(mobile, str):
        return False

    return re.match(MOBILE_REGEX, mobile) is not None


# -----------------------------
# National Code Validation
# -----------------------------
def validate_national_code(code: str) -> bool:
    """
    Validate Iranian national code (basic algorithm).
    """
    if not isinstance(code, str) or not code.isdigit() or len(code) != 10:
        return False

    if len(set(code)) == 1:
        return False

    check = int(code[9])
    sum_ = sum(int(code[i]) * (10 - i) for i in range(9))
    remainder = sum_ % 11

    return (remainder < 2 and check == remainder) or (
        remainder >= 2 and check == (11 - remainder)
    )


# -----------------------------
# File Validation
# -----------------------------
ALLOWED_EXTENSIONS = {
    "jpg", "jpeg", "png",
    "pdf", "doc", "docx",
    "xlsx", "zip", "rar"
}


def validate_file(filename: str, max_size: int, file_size: int) -> bool:
    """
    Validate uploaded file.
    """

    if not isinstance(filename, str):
        return False

    if file_size > max_size:
        return False

    if "." not in filename:
        return False

    ext = filename.rsplit(".", 1)[-1].lower()

    return ext in ALLOWED_EXTENSIONS


# -----------------------------
# General Text Validation
# -----------------------------
def validate_text(text: str, max_length: int = 3000) -> bool:
    """
    Validate user text input.
    """
    if not isinstance(text, str):
        return False

    if len(text.strip()) == 0:
        return False

    if len(text) > max_length:
        return False

    return True


# -----------------------------
# Tracking Search Input
# -----------------------------
def is_tracking_query(text: str) -> bool:
    """
    Detect if input is tracking code.
    """
    return validate_tracking(text.strip() if isinstance(text, str) else "")
