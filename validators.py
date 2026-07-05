"""
validators.py

Input validators for Azarakhsh.
"""

import re


# -----------------------------
# Request Number
# -----------------------------
def validate_request_number(value: str) -> bool:
    """
    11 digits.
    """

    return bool(
        re.fullmatch(
            r"\d{11}",
            value,
        )
    )


# -----------------------------
# Computer Code
# -----------------------------
def validate_computer_code(value: str) -> bool:
    """
    7 digits.
    """

    return bool(
        re.fullmatch(
            r"\d{7}",
            value,
        )
    )


# -----------------------------
# Mobile
# -----------------------------
def validate_mobile(value: str) -> bool:
    """
    10 digits without leading zero.
    Starts with 9.
    """

    return bool(
        re.fullmatch(
            r"9\d{9}",
            value,
        )
    )


# -----------------------------
# Bill ID
# -----------------------------
def validate_bill_id(value: str) -> bool:
    """
    13 digits.
    Starts with 1.
    """

    return bool(
        re.fullmatch(
            r"1\d{12}",
            value,
        )
    )


# -----------------------------
# National Code
# -----------------------------
def validate_national_code(value: str) -> bool:
    """
    Validate Iranian national code.
    """

    if not re.fullmatch(r"\d{10}", value):
        return False

    if value == value[0] * 10:
        return False

    digits = list(map(int, value))

    checksum = digits[-1]

    total = sum(
        digits[i] * (10 - i)
        for i in range(9)
    )

    remainder = total % 11

    if remainder < 2:
        return checksum == remainder

    return checksum == (11 - remainder)
