REQUEST_NUMBER = "REQUEST_NUMBER"
MOBILE = "MOBILE"
NATIONAL_CODE = "NATIONAL_CODE"
COMPUTER_CODE = "COMPUTER_CODE"
BILL_ID = "BILL_ID"


def is_numeric(value):
    return value.isdigit()


def validate_mobile(value):
    return (
        len(value) == 10
        and value.startswith("9")
        and value.isdigit()
    )


def validate_request_number(value):
    return len(value) == 11 and value.isdigit()


def validate_bill_id(value):
    return len(value) == 13 and value.isdigit()


def validate_computer_code(value):
    return len(value) == 7 and value.isdigit()


def validate_national_code(code):

    if len(code) != 10:
        return False

    if not code.isdigit():
        return False

    # جلوگیری از کدهای تکراری
    if code == code[0] * 10:
        return False

    check = int(code[9])

    s = sum(
        int(code[i]) * (10 - i)
        for i in range(9)
    )

    r = s % 11

    if r < 2:
        return check == r

    return check == (11 - r)


def detect_identifier(value):

    value = value.strip()

    if validate_computer_code(value):
        return COMPUTER_CODE

    if validate_mobile(value):
        return MOBILE

    if validate_national_code(value):
        return NATIONAL_CODE

    if validate_request_number(value):
        return REQUEST_NUMBER

    if validate_bill_id(value):
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
