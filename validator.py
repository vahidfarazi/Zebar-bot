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

    # شماره موبایل یا کد ملی
    if len(value) == 10:

        # شماره موبایل ایران بدون صفر
        if value.startswith("9"):
            return "MOBILE"

        # سایر اعداد 10 رقمی = کد ملی
        return "NATIONAL_CODE"

    return None
