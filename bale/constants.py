"""
bale/constants.py

Bale API constants.
"""

from config import Config


# -----------------------------
# Bot
# -----------------------------
BOT_TOKEN = Config.get_str("BOT_TOKEN")

BASE_URL = (
    f"https://tapi.bale.ai/bot{BOT_TOKEN}"
)


# -----------------------------
# API Methods
# -----------------------------
SEND_MESSAGE = "/sendMessage"

EDIT_MESSAGE = "/editMessageText"

DELETE_MESSAGE = "/deleteMessage"

ANSWER_CALLBACK = "/answerCallbackQuery"


# -----------------------------
# Parse Mode
# -----------------------------
PARSE_MODE_HTML = "HTML"

PARSE_MODE_MARKDOWN = "Markdown"
