"""
bale_client.py

Official Bale Bot API client (HTTP-based).
"""

import requests

from config import Config
from logger import log_error, log_info


# -----------------------------
# Send Message
# -----------------------------
def send_message(chat_id: int, text: str) -> bool:
    """
    Send message via Bale Bot API.
    """

    base_url = Config.get_str(
        "BALE_API_URL",
        "https://tapi.bale.ai",
    )

    bot_token = Config.get_str(
        "BALE_BOT_TOKEN",
        "",
    )

    if not bot_token:
        log_error(
            "bale_client",
            "missing_token",
            "BALE_BOT_TOKEN is not set",
        )
        return False

    try:

        url = f"{base_url}/bot{bot_token}/sendMessage"

        payload = {
            "chat_id": chat_id,
            "text": text,
        }

        response = requests.post(
            url,
            json=payload,
            timeout=10,
        )

        if response.status_code != 200:

            log_error(
                "bale_client",
                "send_failed",
                f"{response.status_code}: {response.text}",
            )

            return False

        log_info(
            "bale_client",
            "send_message",
            str(chat_id),
        )

        return True

    except Exception as e:

        log_error(
            "bale_client",
            "exception",
            str(e),
        )

        return False
