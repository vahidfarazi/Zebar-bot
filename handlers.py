from flask import Flask, request
import requests

from database import (
    get_user,
    create_user,
    update_state,
    update_service,
    write_log,
)

import states

from keyboards import (
    main_keyboard,
    back_keyboard,
    after_sale_keyboard,
)

from core.messages import (
    WELCOME,
    OUT_OF_TIME,
    HOLIDAY,
    MAINTENANCE,
)

from core.settings import (
    SYSTEM_MODE,
    ALLOW_NEW_REQUEST,
    ALLOW_STATUS,
)

from core.utils import is_work_time


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
        json=data)
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
