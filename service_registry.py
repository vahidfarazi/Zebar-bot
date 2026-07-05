"""
service_registry.py

Central registry for all request services.
"""

from menus import (
    REQUEST_MENU,
    AFTER_SALES_MENU,
)

from form_registry import get_form


SERVICES = {

    "🔌 نصب انشعاب جدید": {
        "service": "NEW_CONNECTION",
    },

    "🔍 بازرسی و تست کنتور": {
        "service": "METER_TEST",
    },

    "🧾 بررسی قبض برق": {
        "service": "BILL",
    },

}


AFTER_SALES = {

    "❓ نوع درخواست خود را نمی‌دانم": "UNKNOWN",

    "🔧 اصلاح سرویس": "SERVICE_FIX",

    "🔵 نصب مجدد": "REINSTALL",

    "📍 تغییر مکان": "RELOCATION",

    "👤 تغییر نام": "CHANGE_NAME",

    "⚡ تبدیل آمپراژ": "AMPERAGE",

    "⏸ جمع‌آوری موقت": "TEMP_REMOVE",

    "❌ جمع‌آوری دائم": "PERMANENT_REMOVE",

}


# -----------------------------
# Get Service
# -----------------------------
def get_service(message: str):

    return SERVICES.get(message)


# -----------------------------
# After Sales
# -----------------------------
def get_after_sales(message: str):

    code = AFTER_SALES.get(message)

    if code is None:
        return None

    return {

        "service": "AFTER_SALES",

        "sub_service": code,

    }
