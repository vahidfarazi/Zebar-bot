"""
bale_client.py

Simple Bale bot client (HTTP API wrapper).
"""

import requests
from config import Config
from logger import log_error


# -----------------------------
# Base Config
# -----------------------------
BASE_URL = Config.get_str("BALE_API_URL", "")
BOT_TOKEN = Config.get_str("BALE_BOT_TOKEN", "")


# -----------------------------
# Send Message
# -----------------------------
def send_message(chat_id: int, text: str) -> bool:
    """
    Send message to Bale chat.
    """

    try:

        if not BASE_URL or not BOT_TOKEN:
            log_error(
                "bale_client",
                "config_missing",
                "BALE_API_URL or BALE_BOT_TOKEN not set",
            )
            return False

        url = f"{BASE_URL}/bot{BOT_TOKEN}/sendMessage"

        payload = {
            "chat_id": chat_id,
            "text": text,
        }

        response = requests.post(url, json=payload, timeout=10)

        if response.status_code != 200:
            log_error(
                "bale_client",
                "send_failed",
                response.text,
            )
            return False

        return True

    except Exception as e:

        log_error(
            "bale_client",
            "exception",
            str(e),
        )

        return False
