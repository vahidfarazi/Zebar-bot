from flask import Flask, request
import requests

app = Flask(__name__)

BOT_TOKEN = "556379301:NglRetfSzjd1xWGqgyA4De3IzlNHheJB98s"
BASE_URL = f"https://tapi.bale.ai/bot{BOT_TOKEN}"

# ارسال پیام
def send_message(chat_id, text):
    requests.post(
        BASE_URL + "/sendMessage",
        json={
            "chat_id": chat_id,
            "text": text
        }
    )

# تست اجرا
@app.route("/", methods=["GET"])
def home():
    return "Bot is running"

# دریافت پیام از بله
@app.route("/webhook", methods=["POST"])
def webhook():
    print("=================================")
    print("NEW REQUEST FROM BALE")
    print(request.json)
    print("=================================")

    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
