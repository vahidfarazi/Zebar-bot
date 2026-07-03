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

    if text in ["/start", "شروع", "🏠 منوی اصلی"]:

        users[chat_id]["state"] = states.MAIN_MENU

        send_message(
            chat_id,
            WELCOME_MESSAGE,
            main_keyboard()
        )

        return

    if text == "🏡 انشعاب جدید":

        users[chat_id]["state"] = states.NEW_CONNECTION

        send_message(
            chat_id,
            """لطفاً یکی از موارد زیر را ارسال نمایید.

• شماره تقاضا (11 رقم)

• شماره موبایل (10 رقم بدون صفر)

• کد ملی (10 رقم)
""",
            back_keyboard()
        )

        return

    if text == "🔧 خدمات پس از فروش":

        send_message(
            chat_id,
            "لطفاً نوع خدمت را انتخاب نمایید.",
            after_sale_keyboard()
        )

        return

    if text in AFTER_SALE_ITEMS:

        users[chat_id]["state"] = states.SERVICE_EDIT

        send_message(
            chat_id,
            f"""خدمت انتخاب شده:

{text}

لطفاً یکی از موارد زیر را ارسال نمایید.

• شماره تقاضا

• شماره موبایل

• کد ملی

• رمز رایانه

• شناسه قبض""",
            back_keyboard()
        )

        return

    if text == "⚡ آزمایش و تست کنتور":

        users[chat_id]["state"] = states.METER_TEST

        send_message(
            chat_id,
            """لطفاً یکی از موارد زیر را ارسال نمایید.

• شماره تقاضا

• شماره موبایل

• کد ملی

• رمز رایانه

• شناسه قبض""",
            back_keyboard()
        )

        return

    if text == "🧾 بررسی قبض برق":

        users[chat_id]["state"] = states.BILL

        send_message(
            chat_id,
            """لطفاً یکی از موارد زیر را ارسال نمایید.

• شماره موبایل (10 رقم بدون صفر)

• رمز رایانه (7 رقم)

• شناسه قبض (13 رقم)
""",
            back_keyboard()
        )

        return

    if text == "📖 راهنما":

        send_message(
            chat_id,
            """برای استفاده از سامانه:

1- یکی از خدمات را انتخاب کنید.

2- فقط شماره یا شناسه خواسته شده را ارسال کنید.

3- از ارسال توضیحات اضافی خودداری کنید.

4- پاسخ کارشناسان از همین طریق برای شما ارسال خواهد شد.""",
            main_keyboard()
        )

        return

    if text == "⬅ بازگشت":

        users[chat_id]["state"] = states.MAIN_MENU

        send_message(
            chat_id,
            WELCOME_MESSAGE,
            main_keyboard()
        )

        return

    send_message(
        chat_id,
        "⚠ لطفاً فقط از دکمه‌های موجود استفاده کنید.",
        main_keyboard()
    )
