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

from database import fetch_one, execute
from logger import log_system, log_warning


# -----------------------------
# Default Config Values
# -----------------------------
DEFAULTS: dict[str, Any] = {
    # System
    "BOT_VERSION": "1.0",
    "TIMEZONE": "Asia/Tehran",
    "SYSTEM_MODE": "NORMAL",

    # Working Hours
    "WORK_START": "07:00",
    "WORK_END": "13:00",

    # Features
    "ALLOW_NEW_REQUEST": "1",
    "ALLOW_TRACKING": "1",
    "ALLOW_CHAT": "1",

    # Limits
    "MAX_UPLOAD_SIZE": "20971520",
    "MAX_MESSAGE_LENGTH": "3000",
    "DEFAULT_PRIORITY": "NORMAL",

    # Directories
    "DB_NAME": "azarakhsh.db",
    "LOG_DIRECTORY": "logs",
    "UPLOAD_DIRECTORY": "uploads",
    "BACKUP_DIRECTORY": "backups",
    "LOG_LEVEL": "INFO",

    # Bale
    "BALE_API_URL": "",
    "BALE_BOT_TOKEN": "",

    # Holidays
    "HOLIDAYS": "",
}


# -----------------------------
# Cache Layer
# -----------------------------
_config_cache: dict[str, Any] = {}


# -----------------------------
# Config Class
# -----------------------------
class Config:
    """
    Central configuration handler.
    """

    @staticmethod
    def _get_from_env(key: str) -> Optional[str]:
        return os.getenv(key)

    @staticmethod
    def _get_from_db(key: str) -> Optional[str]:
        row = fetch_one(
            "SELECT value FROM settings WHERE key = ?",
            (key,),
        )

        return row["value"] if row else None

    @staticmethod
    def _get_default(key: str) -> Any:
        return DEFAULTS.get(key)

    @staticmethod
    def get(key: str, default: Any = None) -> Any:
        """
        Get configuration value.

        Priority:
        Environment -> Database -> Defaults -> Provided default
        """

        if key in _config_cache:
            return _config_cache[key]

        value = (
            Config._get_from_env(key)
            or Config._get_from_db(key)
            or Config._get_default(key)
            or default
        )

        _config_cache[key] = value

        return value

    @staticmethod
    def get_int(key: str, default: int = 0) -> int:
        try:
            return int(Config.get(key, default))
        except (ValueError, TypeError):
            log_warning(
                "config",
                "type_error",
                f"{key} is not an integer"
            )
            return default

    @staticmethod
    def get_bool(key: str, default: bool = False) -> bool:
        value = str(Config.get(key, default)).strip().lower()

        return value in (
            "1",
            "true",
            "yes",
            "on",
        )

    @staticmethod
    def get_str(key: str, default: str = "") -> str:
        return str(Config.get(key, default))

    @staticmethod
    def exists(key: str) -> bool:
        """
        Check whether a configuration key exists.
        """

        return Config.get(key) is not None

    @staticmethod
    def refresh() -> None:
        """
        Clear configuration cache.
        """

        _config_cache.clear()

        log_system(
            "config",
            "refresh",
            "Configuration cache cleared"
        )

    @staticmethod
    def set(key: str, value: Any) -> None:
        """
        Save configuration into database.
        """

        execute(
            """
            INSERT INTO settings (key, value)
            VALUES (?, ?)
            ON CONFLICT(key)
            DO UPDATE SET value = excluded.value
            """,
            (
                key,
                str(value),
            ),
        )

        _config_cache[key] = value

        log_system(
            "config",
            "update",
            f"{key} updated"
                     )
