"""
messages.py

Central message repository for Azarakhsh system.

Rule:
- NO text should exist inside handlers or services.
- All user-facing messages must be defined here.
"""


# -----------------------------
# General Messages
# -----------------------------
WELCOME_MESSAGE = "به سامانه آذرخش خوش آمدید."

SYSTEM_BUSY = "سامانه در حال حاضر در دسترس نیست."

UNAUTHORIZED_ACCESS = "شما مجاز به انجام این عملیات نیستید."

INVALID_INPUT = "ورودی وارد شده معتبر نیست."

UNKNOWN_ERROR = "خطایی در سامانه رخ داده است."


# -----------------------------
# Request Messages
# -----------------------------
REQUEST_CREATED = "درخواست شما ثبت شد."

REQUEST_NOT_FOUND = "درخواستی یافت نشد."

DUPLICATE_REQUEST = "درخواست مشابه قبلاً ثبت شده است."

REQUEST_CLOSED = "درخواست با موفقیت بسته شد."

REQUEST_UPDATED = "وضعیت درخواست بروزرسانی شد."


# -----------------------------
# Tracking Messages
# -----------------------------
INVALID_TRACKING = "شماره رهگیری معتبر نیست."

TRACKING_NOT_FOUND = "درخواستی با این شماره رهگیری یافت نشد."

TRACKING_FORMAT_ERROR = "فرمت شماره رهگیری صحیح نیست."


# -----------------------------
# Working Hours
# -----------------------------
OUT_OF_WORK_TIME = "سامانه در حال حاضر خارج از ساعات کاری است.\nساعات پاسخگویی: 07:00 تا 13:00"

HOLIDAY_MESSAGE = "امروز سامانه تعطیل است."

MAINTENANCE_MODE = "سامانه در حال بروزرسانی است."


# -----------------------------
# File Messages
# -----------------------------
FILE_TOO_LARGE = "حجم فایل بیشتر از حد مجاز است."

INVALID_FILE_TYPE = "فرمت فایل مجاز نیست."

FILE_UPLOAD_FAILED = "ارسال فایل با مشکل مواجه شد."


# -----------------------------
# Permission Messages
# -----------------------------
PERMISSION_DENIED = "دسترسی غیرمجاز."

ADMIN_ONLY = "این بخش فقط برای مدیران قابل دسترسی است."

EXPERT_ONLY = "این بخش فقط برای کارشناسان قابل دسترسی است."


# -----------------------------
# Chat Messages
# -----------------------------
CHAT_ENDED = "گفتگو به پایان رسید."

MESSAGE_SENT = "پیام ارسال شد."

FILE_SENT = "فایل ارسال شد."


# -----------------------------
# Validation Messages
# -----------------------------
INVALID_MOBILE = "شماره موبایل معتبر نیست."

INVALID_NATIONAL_CODE = "کد ملی وارد شده معتبر نیست."


# -----------------------------
# System Messages
# -----------------------------
SUCCESS = "عملیات با موفقیت انجام شد."

FAILED = "عملیات ناموفق بود."

TRY_AGAIN = "لطفاً دوباره تلاش کنید."
