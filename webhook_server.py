"""
webhook_server.py

FastAPI webhook server for Bale bot.
Receives incoming updates and forwards them to main_runner.
"""

from fastapi import FastAPI, Request

from main_runner import handle_update
from logger import log_info, log_error


app = FastAPI()


# -----------------------------
# Health Check
# -----------------------------
@app.get("/")
def health():
    return {"status": "ok"}


# -----------------------------
# Webhook Endpoint
# -----------------------------
@app.post("/webhook")
async def webhook(request: Request):
    """
    Receive updates from Bale.
    """

    try:

        update = await request.json()

        log_info(
            "webhook",
            "update_received",
            str(update.get("update_id", "unknown")),
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
