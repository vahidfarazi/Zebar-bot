def detect_identifier(service, value):

    value = value.strip()

    if not value.isdigit():
        return None

    # شماره تقاضا
    if len(value) == 11:
        return "REQUEST_NO"

    # شناسه قبض
    if len(value) == 13:
        return "BILL_ID"

    # رمز رایانه
    if len(value) == 7:
        return "COMPUTER_CODE"

    # موبایل یا کد ملی
    if len(value) == 10:

        if value.startswith("0"):
            return "NATIONAL_CODE"

        return "MOBILE"

    return None
