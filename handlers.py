import states

from config import WELCOME_MESSAGE

from keyboards import (
    main_keyboard,
    back_keyboard,
    after_sale_keyboard
)

AFTER_SALE_ITEMS = [

    "🤔 نوع خدمت خود را نمی‌دانم",

    "📝 تغییر نام",

    "🔧 اصلاح سرویس",

    "⏸ جمع‌آوری موقت",

    "❌ جمع‌آوری دائم",

    "🔄 نصب مجدد",

    "📍 تغییر مکان",

    "⚡ تبدیل آمپراژ"

]


def handle_message(chat_id, text, users, send_message):

    if chat_id not in users:
        users[chat_id] = {
            "state": states.MAIN_MENU
        }

    # =============================
    # شروع و منوی اصلی
    # =============================

    if text in ["/start", "شروع", "🏠 منوی اصلی"]:

        users[chat_id]["state"] = states.MAIN_MENU

        send_message(
            chat_id,
            WELCOME_MESSAGE,
            main_keyboard()
        )

        return

    # =============================
    # انشعاب جدید
    # =============================

    if text == "🏡 انشعاب جدید":

        users[chat_id]["state"] = states.NEW_CONNECTION

        send_message(
            chat_id,
            """🏡 انشعاب جدید
━━━━━━━━━━━━━━

یکی از موارد زیر را وارد کنید:

• شماره تقاضا

• شماره موبایل (بدون صفر اول)

• کد ملی
""",
            back_keyboard()
        )

        return

    # =============================
    # خدمات پس از فروش
    # =============================

    if text == "🔧 خدمات پس از فروش":

        send_message(
            chat_id,
            """🔧 خدمات پس از فروش
━━━━━━━━━━━━━━

لطفاً نوع خدمت را انتخاب کنید.""",
            after_sale_keyboard()
        )

        return

    # =============================
    # انتخاب نوع خدمت
    # =============================

    if text in AFTER_SALE_ITEMS:

        users[chat_id]["state"] = states.SERVICE_EDIT

        send_message(
            chat_id,
            f"""🔧 خدمات پس از فروش
━━━━━━━━━━━━━━

✅ خدمت انتخاب‌شده:

{text}

یکی از موارد زیر را وارد کنید:

• شماره تقاضا

• شماره موبایل (بدون صفر اول)

• کد ملی

• رمز رایانه

• شناسه قبض
""",
            back_keyboard()
        )

        return

    # =============================
    # آزمایش و تست کنتور
    # =============================

    if text == "⚡ آزمایش و تست کنتور":

        users[chat_id]["state"] = states.METER_TEST

        send_message(
            chat_id,
            """⚡ آزمایش و تست کنتور
━━━━━━━━━━━━━━

یکی از موارد زیر را وارد کنید:

• شماره تقاضا

• شماره موبایل (بدون صفر اول)

• کد ملی

• رمز رایانه

• شناسه قبض
""",
            back_keyboard()
        )

        return

    # =============================
    # بررسی قبض برق
    # =============================

    if text == "🧾 بررسی قبض برق":

        users[chat_id]["state"] = states.BILL

        send_message(
            chat_id,
            """🧾 بررسی قبض برق
━━━━━━━━━━━━━━

یکی از موارد زیر را وارد کنید:

• شماره موبایل (بدون صفر اول)

• رمز رایانه

• شناسه قبض
""",
            back_keyboard()
        )

        return

    # =============================
    # راهنما
    # =============================

    if text == "📖 راهنما":

        send_message(
            chat_id,
            """📖 راهنما
━━━━━━━━━━━━━━

۱- خدمت موردنظر را انتخاب کنید.

۲- فقط یکی از شناسه‌های خواسته‌شده را وارد کنید.

۳- از ارسال توضیحات اضافی خودداری کنید.

۴- پس از بررسی، پاسخ کارشناس از همین طریق برای شما ارسال خواهد شد.
""",
            main_keyboard()
        )

        return

    # =============================
    # بازگشت
    # =============================

    if text == "⬅ بازگشت":

        users[chat_id]["state"] = states.MAIN_MENU

        send_message(
            chat_id,
            WELCOME_MESSAGE,
            main_keyboard()
        )

        return

    # =============================
    # پیام پیش‌فرض
    # =============================

    send_message(
        chat_id,
        """⚠️ لطفاً فقط از دکمه‌های موجود استفاده کنید.

اگر در یکی از بخش‌ها هستید، فقط شماره یا شناسه خواسته‌شده را وارد کنید.""",
        main_keyboard()
    )
