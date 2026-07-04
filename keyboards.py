"""
keyboards.py

Telegram/Bot UI keyboards for Azarakhsh system.
Only UI definitions. No logic allowed.
"""

# -----------------------------
# User Keyboard
# -----------------------------
def main_menu():
    return {
        "keyboard": [
            ["📌 ثبت درخواست"],
            ["🔎 پیگیری درخواست"],
            ["💬 ارسال پیام"]
        ],
        "resize_keyboard": True
    }


# -----------------------------
# Tracking Keyboard
# -----------------------------
def tracking_keyboard():
    return {
        "keyboard": [
            ["🔎 پیگیری"],
            ["🔙 بازگشت"]
        ],
        "resize_keyboard": True
    }


# -----------------------------
# Admin Keyboard
# -----------------------------
def admin_menu():
    return {
        "keyboard": [
            ["👨‍💼 مدیریت کارشناسان"],
            ["📊 مدیریت درخواست‌ها"],
            ["📅 تعطیلات"],
            ["⚙ تنظیمات سیستم"]
        ],
        "resize_keyboard": True
    }


# -----------------------------
# Expert Keyboard
# -----------------------------
def expert_menu():
    return {
        "keyboard": [
            ["📥 درخواست‌های من"],
            ["✍ پاسخ دادن"],
            ["✔ بستن درخواست"]
        ],
        "resize_keyboard": True
    }
