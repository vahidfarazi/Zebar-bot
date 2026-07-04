"""
main_runner.py

Runtime entry for Azarakhsh system.
Responsible for:
- initializing the system
- processing incoming updates
- sending responses to Bale
"""

from router import route_message
from bale_client import send_message

from logger import (
    log_system,
    log_error,
)

from database import init_database
from messages import GENERAL_ERROR


# -----------------------------
# System Initialization
# -----------------------------
def initialize_system() -> None:
    """
    Initialize all required system components.
    """

    init_database()

    log_system(
        "main_runner",
        "startup",
        "System initialized successfully."
    )


# -----------------------------
# Process Incoming Update
# -----------------------------
def process_update(
    chat_id: int,
    message: str,
    role: str = "USER",
) -> str:
    """
    Process one incoming message and send response.
    """

    try:

        response = route_message(
            chat_id=chat_id,
            message=message,
            role=role,
        )

        send_message(
            chat_id=chat_id,
            text=response,
        )

        return response

    except Exception as exc:

        log_error(
            "main_runner",
            "process_update",
            str(exc),
        )

        send_message(
            chat_id=chat_id,
            text=GENERAL_ERROR,
        )

        return GENERAL_ERROR


# -----------------------------
# Mock CLI Runner
# -----------------------------
def run_mock() -> None:
    """
    Simple CLI runner for local testing.
    """

    initialize_system()

    print("Azarakhsh Mock Runner Started")
    print("Press Ctrl+C to exit.\n")

    while True:

        try:

            chat_id = int(input("Chat ID: "))
            role = input("Role (USER/ADMIN/EXPERT): ").strip().upper()
            message = input("Message: ")

            response = process_update(
                chat_id=chat_id,
                message=message,
                role=role,
            )

            print(f"Response: {response}\n")

        except KeyboardInterrupt:

            print("\nStopping...")

            break

        except Exception as exc:

            log_error(
                "main_runner",
                "mock_runner",
                str(exc),
            )


# -----------------------------
# Entry Point
# -----------------------------
if __name__ == "__main__":

    run_mock()
