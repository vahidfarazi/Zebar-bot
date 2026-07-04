"""
messages.py

All system messages for Azarakhsh Project.

Rule:
- No UI text is allowed outside this file.
"""

from __future__ import annotations


# ---------------- GENERAL ---------------- #

WELCOME_MESSAGE = """
به سامانه آذرخش خوش آمدید.

لطفاً یکی از گزینه‌های زیر را انتخاب کنید.
"""

GOODBYE_MESSAGE = """
از استفاده شما از سامانه متشکریم.
"""

# ---------------- REQUEST ---------------- #

REQUEST_CREATED = """
درخواست شما با موفقیت ثبت شد.

شماره رهگیری:
{tracking_code}
"""

REQUEST_NOT_FOUND = """
درخواستی با این شماره رهگیری یافت نشد.
"""

REQUEST_CLOSED = """
درخواست با موفقیت بسته شد.
"""

DUPLICATE_REQUEST = """
درخواست مشابه قبلاً ثبت شده است.
"""

# ---------------- TRACKING ---------------- #

INVALID_TRACKING = """
شماره رهگیری معتبر نیست.
"""

TRACKING_NOT_FOUND = """
درخواستی با این شماره رهگیری یافت نشد.
"""

# ---------------- WORKING HOURS ---------------- #

OUT_OF_WORK_TIME = """
سامانه در حال حاضر خارج از ساعات کاری است.

ساعات پاسخگویی:
07:00 الی 13:00
"""

HOLIDAY_MESSAGE = """
امروز سامانه تعطیل است.
"""

MAINTENANCE_MODE = """
سامانه در حال بروزرسانی است.
"""

# ---------------- SECURITY ---------------- #

PERMISSION_DENIED = """
شما مجاز به انجام این عملیات نیستید.
"""

EXPERT_ACCESS_DENIED = """
دسترسی غیرمجاز.
"""

RATE_LIMIT_MESSAGE = """
تعداد درخواست‌های شما بیش از حد مجاز است.
"""

# ---------------- FILE ---------------- #

FILE_TOO_LARGE = """
حجم فایل بیشتر از حد مجاز است.
"""

INVALID_FILE_TYPE = """
فرمت فایل مجاز نیست.
"""

FILE_DOWNLOAD_ERROR = """
دریافت فایل با مشکل مواجه شد.
"""

# ---------------- SYSTEM ---------------- #

GENERAL_ERROR = """
خطایی در سامانه رخ داده است.
"""

NETWORK_ERROR = """
مشکلی در ارتباط با سرویس رخ داده است.
"""

TIMEOUT_ERROR = """
پاسخی از سرور دریافت نشد. لطفاً دوباره تلاش کنید.
"""
