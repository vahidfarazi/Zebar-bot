"""
config.py

Central configuration manager for Azarakhsh system.

Priority order:
1. Environment variables
2. Database settings table
3. Default values
"""

import os
from typing import Any, Optional
from database import fetch_one, fetch_all, execute
from logger import log_system, log_warning


# -----------------------------
# Default Config Values
# -----------------------------
DEFAULTS: dict[str, Any] = {
    "BOT_VERSION": "1.0",
    "TIMEZONE": "Asia/Tehran",

    "WORK_START": "07:00",
    "WORK_END": "13:00",

    "SYSTEM_MODE": "NORMAL",

    "ALLOW_NEW_REQUEST": "1",
    "ALLOW_TRACKING": "1",
    "ALLOW_CHAT": "1",

    "MAX_UPLOAD_SIZE": "20971520",
    "MAX_MESSAGE_LENGTH": "3000",
    "DEFAULT_PRIORITY": "NORMAL",
}


# -----------------------------
# Cache Layer
# -----------------------------
_CACHE: dict[str, Any] = {}


# -----------------------------
# Config Class
# -----------------------------
class Config:
    """
    Central configuration handler.
    """

    # -------------------------
    # Internal Loaders
    # -------------------------
    @staticmethod
    def _get_from_env(key: str) -> Optional[str]:
        return os.getenv(key)

    @staticmethod
    def _get_from_db(key: str) -> Optional[str]:
        row = fetch_one(
            "SELECT value FROM settings WHERE key = ?",
            (key,)
        )
        return row["value"] if row else None

    @staticmethod
    def _get_default(key: str) -> Any:
        return DEFAULTS.get(key)

    # -------------------------
    # Main Getter
    # -------------------------
    @staticmethod
    def get(key: str, default: Any = None) -> Any:
        """
        Get config value with priority:
        ENV → DB → DEFAULT
        """

        # Cache first
        if key in _CACHE:
            return _CACHE[key]

        value = (
            Config._get_from_env(key)
            or Config._get_from_db(key)
            or Config._get_default(key)
            or default
        )

        _CACHE[key] = value

        return value

    # -------------------------
    # Typed Helpers
    # -------------------------
    @staticmethod
    def get_int(key: str, default: int = 0) -> int:
        try:
            return int(Config.get(key, default))
        except Exception:
            log_warning("config", "type_error", f"{key} not int")
            return default

    @staticmethod
    def get_bool(key: str, default: bool = False) -> bool:
        value = str(Config.get(key, default)).lower()
        return value in ("1", "true", "yes", "on")

    @staticmethod
    def get_str(key: str, default: str = "") -> str:
        return str(Config.get(key, default))

    # -------------------------
    # Cache Control
    # -------------------------
    @staticmethod
    def refresh() -> None:
        """
        Clear config cache (use after settings update)
        """
        _CACHE.clear()
        log_system("config", "refresh", "Config cache cleared")

    # -------------------------
    # Set Config (Admin use)
    # -------------------------
    @staticmethod
    def set(key: str, value: Any) -> None:
        """
        Save config to database.
        """
        execute("""
            INSERT INTO settings (key, value)
            VALUES (?, ?)
            ON CONFLICT(key) DO UPDATE SET value = excluded.value
        """, (key, str(value)))

        _CACHE[key] = value

        log_system("config", "update", f"{key} updated")
