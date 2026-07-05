"""
logger.py

Central logging system for Azarakhsh.
"""

from database import execute


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
    Save log into database.

    Logging must NEVER crash application.
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

        # fallback console log
        print(
            f"[{level}] {module}.{action}: {description}"
        )


# -----------------------------
# Public Loggers
# -----------------------------
def log_system(
    module: str,
    action: str,
    description: str,
) -> None:
    _write_log("SYSTEM", module, action, description)


def log_info(
    module: str,
    action: str,
    description: str,
) -> None:
    _write_log("INFO", module, action, description)


def log_warning(
    module: str,
    action: str,
    description: str,
) -> None:
    _write_log("WARNING", module, action, description)


def log_error(
    module: str,
    action: str,
    description: str,
) -> None:
    _write_log("ERROR", module, action, description)


def log_security(
    module: str,
    action: str,
    description: str,
) -> None:
    _write_log("SECURITY", module, action, description)


def log_admin(
    module: str,
    action: str,
    description: str,
) -> None:
    _write_log("ADMIN", module, action, description)


def log_critical(
    module: str,
    action: str,
    description: str,
) -> None:
    _write_log("CRITICAL", module, action, description)


# -----------------------------
# Debug
# -----------------------------
def debug(message: str) -> None:
    """
    Simple debug output.
    """

    print(f"[DEBUG] {message}")
