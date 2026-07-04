"""
logger.py

Central logging system for Azarakhsh.

Supports:
- system logs
- info logs
- warning logs
- error logs
- security logs
- admin logs
- critical logs
"""

from database import execute
from config import Config


# -----------------------------
# Base Logger
# -----------------------------
def _write_log(
    level: str,
    module: str,
    action: str,
    description: str,
) -> None:
    """
    Write log entry into database.
    """

    try:

        execute(
            """
            INSERT INTO system_logs
            (
                level,
                module,
                action,
                description
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                level,
                module,
                action,
                description,
            ),
        )

    except Exception:
        # Never allow logging failures
        # to interrupt the application.
        pass


# -----------------------------
# System Logs
# -----------------------------
def log_system(
    module: str,
    action: str,
    description: str,
) -> None:
    _write_log(
        "SYSTEM",
        module,
        action,
        description,
    )


# -----------------------------
# Info Logs
# -----------------------------
def log_info(
    module: str,
    action: str,
    description: str,
) -> None:
    _write_log(
        "INFO",
        module,
        action,
        description,
    )


# -----------------------------
# Warning Logs
# -----------------------------
def log_warning(
    module: str,
    action: str,
    description: str,
) -> None:
    _write_log(
        "WARNING",
        module,
        action,
        description,
    )


# -----------------------------
# Error Logs
# -----------------------------
def log_error(
    module: str,
    action: str,
    description: str,
) -> None:
    _write_log(
        "ERROR",
        module,
        action,
        description,
    )


# -----------------------------
# Security Logs
# -----------------------------
def log_security(
    module: str,
    action: str,
    description: str,
) -> None:
    _write_log(
        "SECURITY",
        module,
        action,
        description,
    )


# -----------------------------
# Admin Logs
# -----------------------------
def log_admin(
    module: str,
    action: str,
    description: str,
) -> None:
    _write_log(
        "ADMIN",
        module,
        action,
        description,
    )


# -----------------------------
# Critical Logs
# -----------------------------
def log_critical(
    module: str,
    action: str,
    description: str,
) -> None:
    _write_log(
        "CRITICAL",
        module,
        action,
        description,
    )


# -----------------------------
# Debug Output
# -----------------------------
def debug(message: str) -> None:
    """
    Print debug message only when DEBUG_MODE is enabled.
    """

    if Config.get_bool("DEBUG_MODE", False):
        print(f"[DEBUG] {message}")
