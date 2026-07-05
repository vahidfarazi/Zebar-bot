"""
forms.py

Request forms definition for Azarakhsh.
"""

# -----------------------------
# New Connection
# -----------------------------
NEW_CONNECTION_FORM = [
    {
        "field": "request_number",
        "state": "WAIT_REQUEST_NUMBER",
        "title": "شماره تقاضا",
        "validator": "request_number",
    },
    {
        "field": "national_code",
        "state": "WAIT_NATIONAL_CODE",
        "title": "کد ملی",
        "validator": "national_code",
    },
    {
        "field": "mobile",
        "state": "WAIT_MOBILE",
        "title": "شماره تلفن همراه",
        "validator": "mobile",
    },
]


# -----------------------------
# After Sales
# -----------------------------
AFTER_SALES_FORM = [
    {
        "field": "computer_code",
        "state": "WAIT_COMPUTER_CODE",
        "title": "رمز رایانه",
        "validator": "computer_code",
    },
    {
        "field": "bill_id",
        "state": "WAIT_BILL_ID",
        "title": "شناسه قبض",
        "validator": "bill_id",
    },
    {
        "field": "request_number",
        "state": "WAIT_REQUEST_NUMBER",
        "title": "شماره تقاضا",
        "validator": "request_number",
    },
    {
        "field": "national_code",
        "state": "WAIT_NATIONAL_CODE",
        "title": "کد ملی",
        "validator": "national_code",
    },
    {
        "field": "mobile",
        "state": "WAIT_MOBILE",
        "title": "شماره تلفن همراه",
        "validator": "mobile",
    },
]


# -----------------------------
# Meter Test
# -----------------------------
METER_TEST_FORM = [
    {
        "field": "request_number",
        "state": "WAIT_REQUEST_NUMBER",
        "title": "شماره تقاضا",
        "validator": "request_number",
    },
    {
        "field": "computer_code",
        "state": "WAIT_COMPUTER_CODE",
        "title": "رمز رایانه",
        "validator": "computer_code",
    },
    {
        "field": "bill_id",
        "state": "WAIT_BILL_ID",
        "title": "شناسه قبض",
        "validator": "bill_id",
    },
    {
        "field": "mobile",
        "state": "WAIT_MOBILE",
        "title": "شماره تلفن همراه",
        "validator": "mobile",
    },
    {
        "field": "national_code",
        "state": "WAIT_NATIONAL_CODE",
        "title": "کد ملی",
        "validator": "national_code",
    },
]
