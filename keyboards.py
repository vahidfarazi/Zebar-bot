"""
keyboards.py

All keyboards for Azarakhsh system.

Rule:
- NO keyboard should be created inside handlers.
- Each keyboard has a single responsibility.
"""

from typing import List


# -----------------------------
# Base Builder
# -----------------------------
def _build_keyboard(rows: List[List[str]]) -> dict:
    """
    Simple keyboard structure builder.
    (Can be replaced with Telegram/Bale framework later)
    """
    return {"keyboard": rows, "resize_keyboard": True}


# -----------------------------
# MAIN MENU
# -----------------------------
def get_main_menu():
    return _build_keyboard([
        ["📝 ثبت درخواست", "📋 پیگیری درخواست"],
        ["💬 ارتباط با کارشناس", "📚 راهنما"],
        ["ℹ درباره سامانه"]
    ])


# -----------------------------
# SERVICE MENU
# -----------------------------
def get_service_keyboard():
    return _build_keyboard([
        ["⚡ برق", "💧 آب"],
        ["🏢 مشترکین", "💰 مالی"],
        ["🖥 فناوری اطلاعات"],
        ["⬅ بازگشت", "❌ لغو"]
    ])


# -----------------------------
# SUB SERVICE
# -----------------------------
def get_subservice_keyboard():
    return _build_keyboard([
        ["قطع برق", "افت ولتاژ"],
        ["خسارت", "جابجایی کنتور"],
        ["سایر"],
        ["⬅ بازگشت", "❌ لغو"]
    ])


# -----------------------------
# REQUEST CREATED
# -----------------------------
def get_request_created_keyboard():
    return _build_keyboard([
        ["📋 مشاهده وضعیت", "💬 گفتگو"],
        ["🏠 منوی اصلی"]
    ])


# -----------------------------
# CHAT KEYBOARD
# -----------------------------
def get_chat_keyboard():
    return _build_keyboard([
        ["📎 ارسال فایل", "✅ پایان گفتگو"],
        ["🏠 منوی اصلی"]
    ])


# -----------------------------
# TRACKING
# -----------------------------
def get_tracking_keyboard():
    return _build_keyboard([
        ["🔎 جستجو"],
        ["🏠 منوی اصلی"]
    ])


# -----------------------------
# HELP
# -----------------------------
def get_help_keyboard():
    return _build_keyboard([
        ["📞 تماس", "🌐 سایت"],
        ["🏠 منوی اصلی"]
    ])


# -----------------------------
# ADMIN MENU
# -----------------------------
def get_admin_keyboard():
    return _build_keyboard([
        ["📨 درخواست‌ها", "👥 کاربران"],
        ["👨‍💼 کارشناسان", "⚙ تنظیمات"],
        ["📅 تعطیلات", "📈 آمار"],
        ["📜 گزارشات", "📝 لاگ‌ها"]
    ])


# -----------------------------
# ADMIN REQUEST
# -----------------------------
def get_admin_request_keyboard():
    return _build_keyboard([
        ["✅ ارجاع", "✏ تغییر وضعیت"],
        ["❌ بستن", "⬅ بازگشت"]
    ])


# -----------------------------
# ADMIN SETTINGS
# -----------------------------
def get_admin_settings_keyboard():
    return _build_keyboard([
        ["🕐 ساعات کاری", "🚫 غیرفعال کردن سامانه"],
        ["🔄 حالت تعمیرات", "⬅ بازگشت"]
    ])


# -----------------------------
# EXPERT MENU
# -----------------------------
def get_expert_keyboard():
    return _build_keyboard([
        ["📨 درخواست‌های من", "💬 گفتگوها"],
        ["📊 وضعیت", "⬅ خروج"]
    ])


# -----------------------------
# EXPERT CHAT
# -----------------------------
def get_expert_chat_keyboard():
    return _build_keyboard([
        ["📎 ارسال فایل", "✅ بستن درخواست"],
        ["⬅ بازگشت"]
    ])


# -----------------------------
# CONFIRMATION
# -----------------------------
def get_confirm_keyboard():
    return _build_keyboard([
        ["بله", "خیر"]
    ])


# -----------------------------
# CANCEL
# -----------------------------
def get_cancel_keyboard():
    return _build_keyboard([
        ["❌ لغو"]
    ])


# -----------------------------
# BACK
# -----------------------------
def get_back_keyboard():
    return _build_keyboard([
        ["⬅ بازگشت"]
    ])


# -----------------------------
# HOME
# -----------------------------
def get_home_keyboard():
    return _build_keyboard([
        ["🏠 منوی اصلی"]
    ])


# -----------------------------
# EMPTY (Remove Keyboard)
# -----------------------------
def get_remove_keyboard():
    return {"remove_keyboard": True}
