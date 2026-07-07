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
    10 digits.
    """

    return bool(
        re.fullmatch(
            r"\d{10}",
            value,
        )
    )


# -----------------------------
# Subscription
# -----------------------------
def validate_subscription(value: str) -> bool:
    """
    5 digits.
    """

    return bool(
        re.fullmatch(
            r"\d{5}",
            value,
        )
    )


# -----------------------------
# Meter Serial
# -----------------------------
def validate_meter_serial(value: str) -> bool:
    """
    Up to 20 digits.
    """

    return bool(
        re.fullmatch(
            r"\d{1,20}",
            value,
        )
    )


# -----------------------------
# Detect Identifier
# -----------------------------
def detect_identifier(
    value: str,
) -> str | None:
    """
    Detect identifier type.

    Priority:
    mobile
    national_code
    bill_id
    request_number
    computer_code
    subscription
    meter_serial
    """

    if validate_mobile(value):
        return "mobile"

    if validate_national_code(value):
        return "national_code"

    if validate_bill_id(value):
        return "bill_id"

    if validate_request_number(value):
        return "request_number"

    if validate_computer_code(value):
        return "computer_code"

    if validate_subscription(value):
        return "subscription"

    if validate_meter_serial(value):
        return "meter_serial"

    return None
