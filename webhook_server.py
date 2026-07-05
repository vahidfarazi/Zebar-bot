"""
webhook_server.py

FastAPI webhook server for Bale bot.
"""

from fastapi import FastAPI, Request

from main_runner import handle_update
from logger import log_info, log_error

app = FastAPI()


@app.get("/")
def health():
    return {"status": "ok"}


@app.post("/webhook")
async def webhook(request: Request):

    try:

        update = await request.json()

        # لاگ کل داده دریافتی از بله
        log_info(
            "webhook",
            "raw_update",
            str(update),
        )

        handle_update(update)

        return {"ok": True}

    except Exception as e:

        log_error(
            "webhook",
            "exception",
            str(e),
        )

        return {"ok": False}
