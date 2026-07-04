"""
messages.py

Centralized user/system messages for Azarakhsh.
No hard-coded text should exist in handlers or services.
"""

# -----------------------------
# General Messages
# -----------------------------
GENERAL_ERROR = "خطایی در سامانه رخ داده است. لطفاً دوباره تلاش کنید."
INVALID_INPUT = "ورودی نامعتبر است."
ACCESS_DENIED = "شما مجاز به انجام این عملیات نیستید."


# -----------------------------
# Request Messages
# -----------------------------
REQUEST_CREATED = "درخواست شما با موفقیت ثبت شد."
REQUEST_NOT_FOUND = "درخواستی با این مشخصات یافت نشد."
DUPLICATE_REQUEST = "این درخواست قبلاً ثبت شده است."


# -----------------------------
# Tracking Messages
# -----------------------------
INVALID_TRACKING = "شماره رهگیری معتبر نیست."
TRACKING_NOT_FOUND = "درخواستی با این شماره رهگیری یافت نشد."


# -----------------------------
# Working Hours Messages
# -----------------------------
OUT_OF_WORK_TIME = "سامانه در حال حاضر خارج از ساعات کاری است.\nساعات پاسخگویی: 07:00 تا 13:00"

HOLIDAY_MESSAGE = "امروز سامانه تعطیل است."

MAINTENANCE_MODE = "سامانه در حال بروزرسانی است. لطفاً بعداً مراجعه کنید."


# -----------------------------
# User Messages
# -----------------------------
WELCOME_MESSAGE = "به سامانه آذرخش خوش آمدید."
USER_MESSAGE_RECEIVED = "پیام شما دریافت شد."


# -----------------------------
# Expert Messages
# -----------------------------
EXPERT_REPLY_SAVED = "پاسخ شما ثبت شد."
REQUEST_CLOSED = "درخواست با موفقیت بسته شد."


# -----------------------------
# Admin Messages
# -----------------------------
EXPERT_CREATED = "کارشناس با موفقیت اضافه شد."
EXPERT_REMOVED = "کارشناس غیرفعال شد."
SETTINGS_UPDATED = "تنظیمات با موفقیت بروزرسانی شد."
HOLIDAY_ADDED = "تعطیلی ثبت شد."
HOLIDAY_REMOVED = "تعطیلی حذف شد."
REQUEST_TRANSFERRED = "درخواست با موفقیت منتقل شد."


# -----------------------------
# Validation Messages
# -----------------------------
INVALID_FILE = "فایل ارسالی معتبر نیست."
FILE_TOO_LARGE = "حجم فایل بیشتر از حد مجاز است."
INVALID_FILE_TYPE = "فرمت فایل مجاز نیست."
INVALID_TRACKING = "شماره رهگیری اشتباه است."


# -----------------------------
# Security Messages
# -----------------------------
RATE_LIMIT_EXCEEDED = "تعداد درخواست‌های شما بیش از حد مجاز است. لطفاً کمی صبر کنید."
