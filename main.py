"""
main.py

Entry point of Azarakhsh system.
Responsible for:
- starting application
- initializing database
- loading handlers
- running bot loop
"""

from logger import log_system, log_error
from database import init_database
from working_hours import get_current_time, is_working_time
from config import Config
from fix_tracking import fix_tracking_sequence


# -----------------------------
# App Init
# -----------------------------
def initialize_system() -> None:
    """
    Initialize all core components.
    """
    try:

        init_database()

        # Temporary fix:
        # Update tracking sequence once
        fix_tracking_sequence()

        log_system(
            "main",
            "init",
            "Database initialized successfully"
        )

        # Future: init cache, services, etc.

    except Exception as e:

        log_error(
            "main",
            "init_failed",
            str(e)
        )

        raise


# -----------------------------
# Health Check
# -----------------------------
def health_check() -> dict:
    """
    Basic system health status.
    """

    return {
        "status": "ok",
        "time": str(get_current_time()),
        "working_time": is_working_time(),
        "version": Config.get(
            "BOT_VERSION",
            "1.0"
        ),
    }


# -----------------------------
# Main Runner
# -----------------------------
def run_app() -> None:
    """
    Main runtime entry.
    """

    log_system(
        "main",
        "startup",
        "System starting..."
    )

    try:

        initialize_system()

        log_system(
            "main",
            "ready",
            "System is ready"
        )


        # NOTE:
        # In real implementation, webhook server or bot polling starts here.
        # Example:
        # app.run(host="0.0.0.0", port=5000)


        log_system(
            "main",
            "runtime",
            "Azarakhsh system is running"
        )


    except Exception as e:

        log_error(
            "main",
            "fatal",
            str(e)
        )

        raise


# -----------------------------
# Entry Point
# -----------------------------
if __name__ == "__main__":

    run_app()
