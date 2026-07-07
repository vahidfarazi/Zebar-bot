"""
forms.py

Request forms for Azarakhsh.
"""

# -----------------------------
# New Connection
# -----------------------------
NEW_CONNECTION_FORM = [

    {
        "field": "identifier",
        "state": "NEW_CONNECTION_IDENTIFIER",
        "title": (
            "لطفاً یکی از موارد زیر را وارد کنید:\n\n"
            "• شماره موبایل (بدون صفر اول)\n"
            "• شماره تقاضا\n"
            "• کد ملی"
        ),
        "validator": "ONE_OF",
    },

]


# -----------------------------
# After Sales
# -----------------------------
AFTER_SALES_FORM = [

    {
        "field": "identifier",
        "state": "AFTER_SALES_IDENTIFIER",
        "title": (
            "لطفاً یکی از موارد زیر را وارد کنید:\n\n"
            "• شماره موبایل (بدون صفر اول)\n"
            "• سریال کنتور\n"
            "• شماره تقاضا\n"
            "• شناسه قبض\n"
            "• رمز رایانه\n"
            "• اشتراک\n"
            "• کد ملی"
        ),
        "validator": "ONE_OF",
    },

]


# -----------------------------
# Meter Test
# -----------------------------
METER_TEST_FORM = [

    {
        "field": "identifier",
        "state": "METER_TEST_IDENTIFIER",
        "title": (
            "لطفاً یکی از موارد زیر را وارد کنید:\n\n"
            "• شماره موبایل (بدون صفر اول)\n"
            "• سریال کنتور\n"
            "• شماره تقاضا\n"
            "• شناسه قبض\n"
            "• رمز رایانه\n"
            "• اشتراک\n"
            "• کد ملی"
        ),
        "validator": "ONE_OF",
    },

]


# -----------------------------
# Bill Inquiry
# -----------------------------
BILL_INQUIRY_FORM = [

    {
        "field": "identifier",
        "state": "BILL_INQUIRY_IDENTIFIER",
        "title": (
            "لطفاً یکی از موارد زیر را وارد کنید:\n\n"
            "• شماره موبایل (بدون صفر اول)\n"
            "• سریال کنتور\n"
            "• شناسه قبض\n"
            "• رمز رایانه\n"
            "• اشتراک"
        ),
        "validator": "ONE_OF",
    },

]
