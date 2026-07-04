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
    "SESSION_TIMEOUT": 3600,
}


class Config:
    """
    Central configuration provider.
    """

    _cache: dict[str, Any] = {}

    @classmethod
    def load(cls) -> None:
        """
        Initialize configuration cache.
        """
        cls._cache = DEFAULT_SETTINGS.copy()

    @classmethod
    def refresh(cls) -> None:
        """
        Reload configuration.
        """
        cls.load()

    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        """
        Get configuration value.

        Environment variable has highest priority.
        """

        env = os.getenv(key)

        if env is not None:
            return env

        return cls._cache.get(key, default)

    @classmethod
    def get_int(cls, key: str) -> int:
        return int(cls.get(key))

    @classmethod
    def get_float(cls, key: str) -> float:
        return float(cls.get(key))

    @classmethod
    def get_bool(cls, key: str) -> bool:
        value = cls.get(key)

        if isinstance(value, bool):
            return value

        return str(value).lower() in (
            "1",
            "true",
            "yes",
            "on",
        )

    @classmethod
    def set(cls, key: str, value: Any) -> None:
        """
        Update cache value.

        Database persistence will be implemented
        in database.py.
        """
        cls._cache[key] = value


Config.load()
