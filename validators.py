"""
validators.py

Input validators for Azarakhsh.
"""

import re


# -----------------------------
# Normalize Digits
# -----------------------------
def normalize_digits(value: str) -> str:
    """
    Convert Persian and Arabic digits to English digits.

    Example:
        ۱۴۰۵۱۱۰۰۰۰۰۱۳
        ->
        1405110000013
    """

    if not value:
        return value

    persian = "۰۱۲۳۴۵۶۷۸۹"
    arabic = "٠١٢٣٤٥٦٧٨٩"
    english = "0123456789"

    translation = str.maketrans(
        persian + arabic,
        english + english,
    )

    return value.translate(
        translation
    )


# -----------------------------
# Request Number
# -----------------------------
def validate_request_number(value: str) -> bool:
    """
    11 digits.
    """

    value = normalize_digits(value)

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

    value = normalize_digits(value)

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

    value = normalize_digits(value)

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

    value = normalize_digits(value)

    return bool(
        re.fullmatch(
            r"1\d{12}",
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

    value = normalize_digits(value)

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

    value = normalize_digits(value)

    return bool(
        re.fullmatch(
            r"\d{1,20}",
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

    value = normalize_digits(value)

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


# -----------------------------
# Detect Identifier
# -----------------------------
def detect_identifier(
    value: str,
) -> str | None:
    """
    Detect identifier type.
    """

    value = normalize_digits(value)

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
