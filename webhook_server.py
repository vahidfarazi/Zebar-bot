"""
webhook_server.py

FastAPI webhook server for Bale bot.
"""

from fastapi import FastAPI, Request

from database import init_database
from logger import log_info, log_error

# -----------------------------
# Initialize Database FIRST
# -----------------------------
init_database()

# بعد از ساخت دیتابیس import کن
from main_runner import handle_update

app = FastAPI()


@app.get("/")
def health():
    return {
        "status": "ok",
    }


@app.post("/webhook")
async def webhook(request: Request):

    try:

        update = await request.json()

        log_info(
            "webhook",
            "raw_update",
            str(update),
        )

        handle_update(update)

        return {
            "ok": True,
        }

    except Exception as e:

        log_error(
            "webhook",
            "exception",
            str(e),
        )

        return {
            "ok": False,
        }
