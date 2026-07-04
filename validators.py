"""
validators.py

Validation layer for Azarakhsh Project.

Responsibilities:
- Input validation
- Format checking
- Security filtering

Rule:
- No database access allowed
"""

from __future__ import annotations

import re
from typing import Any


# ---------------- REGEX PATTERNS ---------------- #

TRACKING_REGEX = r"^SR-[0-9]{4}-[0-9]{7}$"
MOBILE_REGEX = r"^09[0-9]{9}$"
USERNAME_REGEX = r"^[a-zA-Z0-9_]{3,32}$"


# ---------------- TRACKING VALIDATION ---------------- #

def validate_tracking(tracking_code: str) -> bool:
    """
    Validate tracking code format.
    """
    if not tracking_code:
        return False

    return bool(re.match(TRACKING_REGEX, tracking_code))


# ---------------- MOBILE VALIDATION ---------------- #

def validate_mobile(mobile: str) -> bool:
    """
    Validate Iranian mobile number.
    """
    if not mobile:
        return False

    return bool(re.match(MOBILE_REGEX, mobile))


# ---------------- USERNAME VALIDATION ---------------- #

def validate_username(username: str) -> bool:
    """
    Validate username format.
    """
    if not username:
        return False

    return bool(re.match(USERNAME_REGEX, username))


# ---------------- FILE VALIDATION ---------------- #

ALLOWED_EXTENSIONS = {
    "jpg",
    "jpeg",
    "png",
    "pdf",
    "doc",
    "docx",
    "xlsx",
    "zip",
    "rar",
}


def validate_file(filename: str, max_size: int, file_size: int) -> bool:
    """
    Validate uploaded file.
    """

    if not filename or "." not in filename:
        return False

    ext = filename.rsplit(".", 1)[-1].lower()

    if ext not in ALLOWED_EXTENSIONS:
        return False

    if file_size > max_size:
        return False

    return True


# ---------------- GENERIC VALIDATION ---------------- #

def is_empty(value: Any) -> bool:
    """
    Check if value is empty or None.
    """
    if value is None:
        return True

    if isinstance(value, str) and value.strip() == "":
        return True

    return False


def validate_length(value: str, max_length: int) -> bool:
    """
    Validate string length.
    """
    if value is None:
        return False

    return len(value) <= max_length
