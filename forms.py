"""
forms.py

Request forms for Azarakhsh.
"""

# -----------------------------
# New Connection
# -----------------------------
NEW_CONNECTION_FORM = [

    {
        "field": "request_number",
        "state": "NEW_CONNECTION_REQUEST_NUMBER",
        "title": "شماره تقاضا",
        "validator": "request_number",
    },

    {
        "field": "national_code",
        "state": "NEW_CONNECTION_NATIONAL_CODE",
        "title": "کد ملی",
        "validator": "national_code",
    },

    {
        "field": "mobile",
        "state": "NEW_CONNECTION_MOBILE",
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
        "state": "AFTER_SALES_COMPUTER_CODE",
        "title": "رمز رایانه",
        "validator": "computer_code",
    },

    {
        "field": "bill_id",
        "state": "AFTER_SALES_BILL_ID",
        "title": "شناسه قبض",
        "validator": "bill_id",
    },

    {
        "field": "request_number",
        "state": "AFTER_SALES_REQUEST_NUMBER",
        "title": "شماره تقاضا",
        "validator": "request_number",
    },

    {
        "field": "national_code",
        "state": "AFTER_SALES_NATIONAL_CODE",
        "title": "کد ملی",
        "validator": "national_code",
    },

    {
        "field": "mobile",
        "state": "AFTER_SALES_MOBILE",
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
        "state": "METER_TEST_REQUEST_NUMBER",
        "title": "شماره تقاضا",
        "validator": "request_number",
    },

    {
        "field": "computer_code",
        "state": "METER_TEST_COMPUTER_CODE",
        "title": "رمز رایانه",
        "validator": "computer_code",
    },

    {
        "field": "bill_id",
        "state": "METER_TEST_BILL_ID",
        "title": "شناسه قبض",
        "validator": "bill_id",
    },

    {
        "field": "mobile",
        "state": "METER_TEST_MOBILE",
        "title": "شماره تلفن همراه",
        "validator": "mobile",
    },

    {
        "field": "national_code",
        "state": "METER_TEST_NATIONAL_CODE",
        "title": "کد ملی",
        "validator": "national_code",
    },

]
