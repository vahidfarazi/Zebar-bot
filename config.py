"""
config.py

Central configuration manager for Azarakhsh.
Priority:
1. Environment Variables
2. Database
3. Default Values
"""

import os
from typing import Any, Optional

from dotenv import load_dotenv

# -----------------------------
# Load .env
# -----------------------------
load_dotenv()


# -----------------------------
# Default Values
# -----------------------------
DEFAULTS = {
    "BOT_VERSION": "1.0",
    "TIMEZONE": "Asia/Tehran",
    "WORK_START": "07:00",
    "WORK_END": "13:00",
    "SYSTEM_MODE": "NORMAL",
    "ALLOW_NEW_REQUEST": "1",
    "ALLOW_TRACKING": "1",
    "ALLOW_CHAT": "1",
    "DEFAULT_PRIORITY": "NORMAL",
    "MAX_UPLOAD_SIZE": "20971520",
    "MAX_MESSAGE_LENGTH": "3000",
    "BALE_API_URL": "https://tapi.bale.ai",
    "DEBUG_MODE": "0",
}


# -----------------------------
# Cache
# -----------------------------
_CACHE: dict[str, Any] = {}


class Config:

    @staticmethod
    def _env(key: str) -> Optional[str]:
        return os.getenv(key)

    @staticmethod
    def _db(key: str) -> Optional[str]:
        from database.crud import fetch_one

        row = fetch_one(
            """
            SELECT value
            FROM settings
            WHERE key = %s
            """,
            (key,),
        )

        if row is not None:
            return row["value"]

        return None

    @staticmethod
    def get(
        key: str,
        default: Any = None,
    ) -> Any:

        if key in _CACHE:
            return _CACHE[key]

        value = Config._env(key)

        if value is None:
            value = Config._db(key)

        if value is None:
            value = DEFAULTS.get(key)

        if value is None:
            value = default

        _CACHE[key] = value

        return value

    @staticmethod
    def get_str(
        key: str,
        default: str = "",
    ) -> str:

        return str(Config.get(key, default))

    @staticmethod
    def get_int(
        key: str,
        default: int = 0,
    ) -> int:

        try:
            return int(Config.get(key, default))
        except (TypeError, ValueError):
            return default

    @staticmethod
    def get_bool(
        key: str,
        default: bool = False,
    ) -> bool:

        value = str(
            Config.get(key, default)
        ).lower()

        return value in (
            "1",
            "true",
            "yes",
            "on",
        )

    @staticmethod
    def set(
        key: str,
        value: Any,
    ) -> None:

        from database.crud import execute

        execute(
            """
            INSERT INTO settings
            (key, value)
            VALUES (%s, %s)
            ON CONFLICT (key)
            DO UPDATE SET
                value = EXCLUDED.value
            """,
            (
                key,
                str(value),
            ),
        )

        _CACHE[key] = value

    @staticmethod
    def refresh() -> None:

        _CACHE.clear()
