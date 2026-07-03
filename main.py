from flask import Flask, request
import requests

from handlers import handle_message
from database import users

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

    print(data)

    message = data.get("message", {})

    chat_id = message.get("chat", {}).get("id")

    text = message.get("text", "").strip()

    if chat_id and text:
        handle_message(
            chat_id,
            text,
            users,
            send_message
        )

    return "ok"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
