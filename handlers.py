from flask import Flask, request
import requests

import states

from database import (
    get_user,
    create_user,
    update_state,
    update_service,
    write_log,
)

from validator import (
    validate_identifier,
    is_valid_for_service,
)

from request_service import (
    register_request,
)

from system_status import (
    get_system_status,
)

from keyboards import (
    main_keyboard,
    back_keyboard,
    after_sale_keyboard,
)

from core.messages import *

app = Flask(__name__)

BOT_TOKEN = "توکن_بات"

BASE_URL = f"https://tapi.bale.ai/bot{BOT_TOKEN}"


def send_message(chat_id, text, keyboard=None):

    data = {
        "chat_id": chat_id,
        "text": text
    }

    if keyboard:
        data["reply_markup"] = keyboard

    requests.post(
        BASE_URL + "/sendMessage",
        json=data
    )


def system_available(chat_id):

    status = get_system_status()

    if status == "MAINTENANCE":

        send_message(
            chat_id,
            MAINTENANCE
        )

        return False

    if status == "HOLIDAY":

        send_message(
            chat_id,
            HOLIDAY
        )

        return False

    if status == "CLOSED":

        send_message(
            chat_id,
            HOLIDAY
        )

        return False

    return True


@app.route("/")
def home():
    return "Azarakhsh is running"


@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.json

    message = data.get("message", {})

    if not message:
        return "ok"

    chat = message.get("chat", {})

    chat_id = chat.get("id")

    if not chat_id:
        return "ok"

    text = message.get("text", "").strip()

    first_name = message.get("from", {}).get("first_name", "")

    last_name = message.get("from", {}).get("last_name", "")

    username = message.get("from", {}).get("username", "")

    user = get_user(chat_id)

    if user is None:

        create_user(
            chat_id,
            first_name,
            last_name,
            username
        )

        user = get_user(chat_id)

    write_log(chat_id, f"MSG : {text}")
        # ---------------- START ----------------

    if text in ["/start", "شروع"]:

        update_state(
            chat_id,
            states.MAIN_MENU
        )

        send_message(
            chat_id,
            WELCOME,
            main_keyboard()
        )

        return "ok"


    # ---------------- MAIN MENU ----------------

    if text == "🏠 منوی اصلی":

        update_state(
            chat_id,
            states.MAIN_MENU
        )

        send_message(
            chat_id,
            WELCOME,
            main_keyboard()
        )

        return "ok"


    # ---------------- NEW CONNECTION ----------------

    if text == "🔌 نصب انشعاب جدید":

        if not system_available(chat_id):
            return "ok"

        update_state(
            chat_id,
            states.NEW_CONNECTION
        )

        update_service(
            chat_id,
            "NEW_CONNECTION"
        )

        send_message(

            chat_id,

            """لطفاً یکی از موارد زیر را وارد نمایید.

• شماره تقاضا

• شماره موبایل (بدون صفر اول)

• کد ملی
""",

            back_keyboard()

        )

        return "ok"


    # ---------------- AFTER SALE ----------------

    if text == "🔧 خدمات پس از فروش":

        if not system_available(chat_id):
            return "ok"

        update_state(
            chat_id,
            states.AFTER_SALE
        )

        send_message(

            chat_id,

            "لطفاً نوع خدمت را انتخاب نمایید.",

            after_sale_keyboard()

        )

        return "ok"


    # ---------------- METER TEST ----------------

    if text == "⚡ آزمایش و تست کنتور":

        if not system_available(chat_id):
            return "ok"

        update_state(
            chat_id,
            states.METER_TEST
        )

        update_service(
            chat_id,
            "METER_TEST"
        )

        send_message(

            chat_id,

            """لطفاً یکی از موارد زیر را وارد نمایید.

• شماره تقاضا

• شماره موبایل (بدون صفر اول)

• کد ملی

• رمز رایانه

• شناسه قبض
""",

            back_keyboard()

        )

        return "ok"


    # ---------------- BILL ----------------

    if text == "🧾 بررسی قبض برق":

        update_state(
            chat_id,
            states.BILL
        )

        update_service(
            chat_id,
            "BILL"
        )

        send_message(

            chat_id,

            """لطفاً یکی از موارد زیر را وارد نمایید.

• شماره موبایل (بدون صفر اول)

• رمز رایانه

• شناسه قبض
""",

            back_keyboard()

        )

        return "ok"
            # ---------------- AFTER SALE SERVICES ----------------

    after_sale_services = [

        "🤔 نوع خدمت خود را نمی‌دانم",

        "📝 تغییر نام",

        "🔧 اصلاح سرویس",

        "⏸ جمع‌آوری موقت",

        "❌ جمع‌آوری دائم",

        "🔄 نصب مجدد",

        "📍 تغییر مکان",

        "⚡ تبدیل آمپراژ"

    ]


    if text in after_sale_services:

        update_state(
            chat_id,
            states.SERVICE_EDIT
        )

        update_service(
            chat_id,
            "AFTER_SALE",
            text
        )

        send_message(

            chat_id,

            f"""✅ خدمت انتخاب شد:

{text}

لطفاً یکی از موارد زیر را وارد نمایید.

• شماره تقاضا

• شماره موبایل (بدون صفر اول)

• کد ملی

• رمز رایانه

• شناسه قبض
""",

            back_keyboard()

        )

        return "ok"


    # ---------------- GUIDE ----------------

    if text == "📖 راهنما":

        send_message(

            chat_id,

            """برای استفاده از سامانه:

۱- خدمت مورد نظر را انتخاب کنید.

۲- شناسه مربوطه را وارد نمایید.

۳- کد رهگیری را تا پایان فرآیند نزد خود نگه دارید.

۴- از بخش «مشاهده وضعیت درخواست» می‌توانید آخرین وضعیت را مشاهده نمایید.
""",

            main_keyboard()

        )

        return "ok"


    # ---------------- BACK ----------------

    if text == "⬅ بازگشت":

        update_state(
            chat_id,
            states.MAIN_MENU
        )

        send_message(

            chat_id,

            WELCOME,

            main_keyboard()

        )

        return "ok"
            # ---------------- IDENTIFIER INPUT ----------------

    state = user["state"]

    if state in [

        states.NEW_CONNECTION,

        states.METER_TEST,

        states.BILL,

        states.SERVICE_EDIT

    ]:

        result = validate_identifier(text)

        if not result["valid"]:

            send_message(

                chat_id,

                f"❌ {result['message']}",

                back_keyboard()

            )

            return "ok"

        identifier_type = result["type"]

        service = user["service"]

        if not is_valid_for_service(

            service,

            identifier_type

        ):

            send_message(

                chat_id,

                INVALID_FOR_SERVICE,

                back_keyboard()

            )

            return "ok"

        request_result = register_request(

            chat_id=chat_id,

            service=service,

            sub_service=user["sub_service"],

            identifier_type=identifier_type,

            identifier_value=text

        )

        if not request_result["success"]:

            send_message(

                chat_id,

                DUPLICATE_REQUEST.format(

                    tracking=request_result["tracking_code"]

                ),

                main_keyboard()

            )

            update_state(

                chat_id,

                states.MAIN_MENU

            )

            return "ok"

        send_message(

            chat_id,

            REQUEST_REGISTERED.format(

                tracking=request_result["tracking_code"]

            ),

            main_keyboard()

        )

        update_state(

            chat_id,

            states.MAIN_MENU

        )

        write_log(

            chat_id,

            f"NEW REQUEST : {request_result['tracking_code']}"

        )

        return "ok"
            # ---------------- UNKNOWN COMMAND ----------------

    send_message(

        chat_id,

        "⚠️ لطفاً از دکمه‌های موجود استفاده نمایید.",

        main_keyboard()

    )

    return "ok"


if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=8080

    )
