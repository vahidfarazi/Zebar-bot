import re


REQUEST_NUMBER = "REQUEST_NUMBER"
MOBILE = "MOBILE"
NATIONAL_CODE = "NATIONAL_CODE"
COMPUTER_CODE = "COMPUTER_CODE"
BILL_ID = "BILL_ID"


def is_numeric(value):

    return value.isdigit()


def detect_identifier(value):

    value = value.strip()

    if not is_numeric(value):
        return None

    length = len(value)

    # رمز رایانه
    if length == 7:
        return COMPUTER_CODE

    # موبایل بدون صفر
    if length == 10 and value.startswith("9"):
        return MOBILE

    # کد ملی
    if length == 10:
        return NATIONAL_CODE

    # شماره تقاضا
    if length == 11:
        return REQUEST_NUMBER

    # شناسه قبض
    if length == 13:
        return BILL_ID

    return None


def is_valid_for_service(service, identifier_type):

    rules = {

        "NEW_CONNECTION": [

            REQUEST_NUMBER,

            MOBILE,

            NATIONAL_CODE

        ],

        "AFTER_SALE": [

            REQUEST_NUMBER,

            MOBILE,

            NATIONAL_CODE,

            COMPUTER_CODE,

            BILL_ID

        ],

        "METER_TEST": [

            REQUEST_NUMBER,

            MOBILE,

            NATIONAL_CODE,

            COMPUTER_CODE,

            BILL_ID

        ],

        "BILL": [

            MOBILE,

            COMPUTER_CODE,

            BILL_ID

        ]

    }

    if service not in rules:
        return False

    return identifier_type in rules[service]
