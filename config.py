"""
config.py

Central configuration manager for Azarakhsh Project.

Priority:
1. Environment Variables
2. Database Settings
3. Default Values
"""

from __future__ import annotations

import os
from typing import Any

DEFAULT_SETTINGS: dict[str, Any] = {
    # ---------------- BOT ---------------- #
    "BOT_VERSION": "1.0.0",
    "BOT_NAME": "Azarakhsh",
    "WEBHOOK_URL": "",

    # ---------------- SYSTEM ---------------- #
    "SYSTEM_MODE": "NORMAL",
    "WORK_START": "07:00",
    "WORK_END": "13:00",
    "TIMEZONE": "Asia/Tehran",

    "ALLOW_NEW_REQUEST": True,
    "ALLOW_TRACKING": True,
    "ALLOW_CHAT": True,

    # ---------------- FILE ---------------- #
    "MAX_UPLOAD_SIZE": 20 * 1024 * 1024,
    "MAX_MESSAGE_LENGTH": 3000,
    "MAX_FILE_COUNT": 5,

    "UPLOAD_PATH": "uploads",
    "TEMP_PATH": "temp",

    # ---------------- REQUEST ---------------- #
    "DEFAULT_PRIORITY": "NORMAL",

    # ---------------- DATABASE ---------------- #
    "DATABASE_PATH": "database/azarakhsh.db",
    "DATABASE_TIMEOUT": 30,

    # ---------------- LOG ---------------- #
    "LOG_LEVEL": "INFO",
    "LOG_PATH": "logs/app.log",

    # ---------------- SECURITY ---------------- #
    "RATE_LIMIT": 30,
    "SESSION_TIMEOUT": 
