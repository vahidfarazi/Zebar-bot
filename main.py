from flask import Flask, request
import requests

from config import WELCOME_MESSAGE
from keyboards import main_keyboard, back_keyboard
from database import users
import states

app = Flask(__name__)

BOT_TOKEN = "556379301:NglRetfSzjd1xWGqgyA4De3IzlNHheJB98s"
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


@app.route("/")
def home():
    return "Azarakhsh is running"


@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.json

    message = data.get("message", {})

    chat_id = message.get("chat", {}).get("id")

    text = message.get("text", "").strip()

    if not chat_id:
        return "ok"

    if chat_id not in users:
        users[chat_id] = {
            "state": states.MAIN_MENU
        }

    if text == "/start" or text == "شروع":

        users[chat_id]["state"] = states.MAIN_MENU

        send_message(
            chat_id,
            WELCOME_MESSAGE,
            main_keyboard()
        )

        return "ok"

    if text == "🏠 منوی اصلی":

        users[chat_id]["state"] = states.MAIN_MENU

        send_message(
            chat_id,
            WELCOME_MESSAGE,
            main_keyboard()
        )

        return "ok"

    if text == "🔌 نصب انشعاب جدید":

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

        return "ok"

    if text == "🔧 اصلاح سرویس":

        users[chat_id]["state"] = states.SERVICE_EDIT

        send_message(
            chat_id,
            """لطفاً یکی از موارد زیر را ارسال نمایید.

• شماره تقاضا

• شماره موبایل

• کد ملی

• رمز رایانه

• شناسه قبض
""",
            back_keyboard()
        )

        return "ok"

    if text == "⚡ آزمایش و تست کنتور":

        users[chat_id]["state"] = states.METER_TEST

        send_message(
            chat_id,
            """لطفاً یکی از موارد زیر را ارسال نمایید.

• شماره تقاضا

• شماره موبایل

• کد ملی

• رمز رایانه

• شناسه قبض
""",
            back_keyboard()
        )

        return "ok"

    if text == "🧾 بررسی صورتحساب برق":

        users[chat_id]["state"] = states.BILL

        send_message(
            chat_id,
            """لطفاً یکی از موارد زیر را ارسال نمایید.

• رمز رایانه

• شناسه قبض
""",
            back_keyboard()
        )

        return "ok"

    if text == "📖 راهنما":

        send_message(
            chat_id,
            """برای استفاده از سامانه:

1- یکی از خدمات را انتخاب کنید.

2- شناسه موردنظر را ارسال نمایید.

3- منتظر پاسخ کارشناس بمانید.
""",
            main_keyboard()
        )

        return "ok"

    if text == "⬅ بازگشت":

        users[chat_id]["state"] = states.MAIN_MENU

        send_message(
            chat_id,
            WELCOME_MESSAGE,
            main_keyboard()
        )

        return "ok"

    send_message(
        chat_id,
        "⚠ لطفاً از دکمه‌های موجود استفاده نمایید.",
        main_keyboard()
    )

    return "ok"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
