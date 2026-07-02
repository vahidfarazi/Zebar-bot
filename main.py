from flask import Flask, request
import requests

app = Flask(__name__)

BOT_TOKEN = "556379301:NglRetfSzjd1xWGqgyA4De3IzlNHheJB98s"
BASE_URL = f"https://tapi.bale.ai/bot{BOT_TOKEN}"

def send_message(chat_id, text):
    requests.post(BASE_URL + "/sendMessage", json={
        "chat_id": chat_id,
        "text": text
    })

@app.route("/", methods=["GET"])
def home():
    return "Bot is running"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    message = data.get("message", {})
    text = message.get("text", "")
    chat_id = message.get("chat", {}).get("id")

    if text and chat_id:
        send_message(chat_id, "✅ دریافت شد: " + text)

    return "ok"
