"""
logger.py

Central logging system for Azarakhsh.

Supports:
- system logs
- error logs
- security logs
- admin logs
"""

from datetime import datetime, timezone
from database import execute
from config import Config


# -----------------------------
# Time Helper
# -----------------------------
def _now() -> str:
    """
    Return ISO8601 timestamp.
    """
    return datetime.now(timezone.utc).isoformat()


# -----------------------------
# Base Logger
# -----------------------------
def _write_log(level: str, module: str, action: str, description: str) -> None:
    """
    Write log to database.
    """

    try:
        execute("""
            INSERT INTO system_logs (level, module, action, description)
            VALUES (?, ?, ?, ?)
        """, (level, module, action, description))

    except Exception:
        # Prevent logging loop crash
        pass


# -----------------------------
# System Logs
# -----------------------------
def log_system(module: str, action: str, description: str) -> None:
    """
    System-level logs (startup, shutdown, init)
    """
    _write_log("SYSTEM", module, action, description)


def log_info(module: str, action: str, description: str) -> None:
    """
    Info logs
    """
    _write_log("INFO", module, action, description)


def log_warning(module: str, action: str, description: str) -> None:
    """
    Warning logs
    """
    _write_log("WARNING", module, action, description)


def log_error(module: str, action: str, description: str) -> None:
    """
    Error logs
    """
    _write_log("ERROR", module, action, description)


# -----------------------------
# Security Logs
# -----------------------------
def log_security(module: str, action: str, description: str) -> None:
    """
    Security-related events
    """
    _write_log("SECURITY", module, action, description)


# -----------------------------
# Admin Logs
# -----------------------------
def log_admin(module: str, action: str, description: str) -> None:
    """
    Admin operations
    """
    _write_log("ADMIN", module, action, description)


# -----------------------------
# System Critical Wrapper
# -----------------------------
def log_critical(module: str, action: str, description: str) -> None:
    """
    Critical failures (system risk)
    """
    _write_log("CRITICAL", module, action, description)


# -----------------------------
# Console Debug (optional dev mode)
# -----------------------------
def debug(message: str) -> None:
    """
    Print only in development mode.
    """
    if Config.get_bool("DEBUG_MODE", False):
        print(f"[DEBUG] {message}")
