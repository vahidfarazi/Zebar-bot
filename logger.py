"""
logger.py

Central logging system for Azarakhsh Project.

Supports:
- INFO
- WARNING
- ERROR
- CRITICAL
- SECURITY
- SYSTEM
- ADMIN
"""

from __future__ import annotations

import logging
import os
from datetime import datetime

from config import Config


class Logger:
    """
    Central application logger.
    """

    _logger: logging.Logger | None = None

    @classmethod
    def _init_logger(cls) -> logging.Logger:
        """
        Initialize logging configuration.
        """

        logger = logging.getLogger("azarakhsh")
        logger.setLevel(logging.DEBUG)

        if logger.handlers:
            return logger

        log_path = Config.get("LOG_PATH", "logs/app.log")

        os.makedirs(os.path.dirname(log_path), exist_ok=True)

        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S",
        )

        # File handler
        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        # Console handler (optional)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger

    @classmethod
    def get_logger(cls) -> logging.Logger:
        """
        Return singleton logger instance.
        """
        if cls._logger is None:
            cls._logger = cls._init_logger()
        return cls._logger

    # ---------------- CORE LOG METHODS ---------------- #

    @classmethod
    def info(cls, module: str, message: str) -> None:
        cls.get_logger().info(f"{module} | {message}")

    @classmethod
    def warning(cls, module: str, message: str) -> None:
        cls.get_logger().warning(f"{module} | {message}")

    @classmethod
    def error(cls, module: str, message: str) -> None:
        cls.get_logger().error(f"{module} | {message}")

    @classmethod
    def critical(cls, module: str, message: str) -> None:
        cls.get_logger().critical(f"{module} | {message}")

    # ---------------- SPECIAL LOG TYPES ---------------- #

    @classmethod
    def security(cls, module: str, message: str) -> None:
        cls.get_logger().warning(f"SECURITY | {module} | {message}")

    @classmethod
    def system(cls, module: str, message: str) -> None:
        cls.get_logger().info(f"SYSTEM | {module} | {message}")

    @classmethod
    def admin(cls, module: str, message: str) -> None:
        cls.get_logger().info(f"ADMIN | {module} | {message}")

    # ---------------- EXCEPTION HANDLING ---------------- #

    @classmethod
    def exception(cls, module: str, error: Exception) -> None:
        cls.get_logger().error(
            f"{module} | EXCEPTION | {type(error).__name__}: {str(error)}"
        )


# Convenience functions (طبق استاندارد پروژه)
def log_info(module: str, message: str) -> None:
    Logger.info(module, message)


def log_warning(module: str, message: str) -> None:
    Logger.warning(module, message)


def log_error(module: str, message: str) -> None:
    Logger.error(module, message)


def log_security(module: str, message: str) -> None:
    Logger.security(module, message)


def log_system(module: str, message: str) -> None:
    Logger.system(module, message)


def log_admin(module: str, message: str) -> None:
    Logger.admin(module, message)
