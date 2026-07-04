"""
bale_client.py

Client for sending messages to Bale messenger API.
Separates external communication from business logic.
"""

import requests
from logger import log_info, log_error
from config import Config


# -----------------------------
# Send Message
# -----------------------------
def send_message(chat_id: int, text: str) -> bool:
    """
    Send message to Bale user.
    """

    try:
        base_url = Config.get("BALE_API_URL")
        token = Config.get("BALE_BOT_TOKEN")

        url = f"{base_url}/bot{token}/sendMessage"

        payload = {
            "chat_id": chat_id,
            "text": text
        }

        response = requests.post(url, json=payload, timeout=10)

        if response.status_code == 200:
            log_info("bale_client", "send_message", f"sent to {chat_id}")
            return True

        log_error(
            "bale_client",
            "send_failed",
            f"{response.status_code} - {response.text}"
        )

        return False

    except Exception as e:
        log_error("bale_client", "exception", str(e))
        return False
