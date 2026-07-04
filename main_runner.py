"""
main_runner.py

Runtime entry for Azarakhsh bot system.
Connects incoming updates to router.
"""

from router import route_message
from logger import log_system, log_error
from main import initialize_system


# -----------------------------
# Process Incoming Message
# -----------------------------
def process_update(chat_id: int, message: str, role: str = "USER") -> str:
    """
    Entry point for each incoming message.
    """

    try:
        response = route_message(chat_id, message, role)
        return response

    except Exception as e:
        log_error("runner", "process_update", str(e))
        return "خطایی در پردازش پیام رخ داد."


# -----------------------------
# Simulated Bot Loop (MVP)
# -----------------------------
def run_mock_bot():
    """
    Simple CLI simulation for testing system.
    """

    initialize_system()
    log_system("runner", "start", "Mock bot started")

    print("Azarakhsh Bot is running (mock mode)...")

    while True:
        try:
            chat_id = int(input("\nChat ID: "))
            message = input("Message: ")
            role = input("Role (USER/ADMIN/EXPERT): ").upper()

            response = process_update(chat_id, message, role)

            print("\nRESPONSE:")
            print(response)

        except KeyboardInterrupt:
            print("\nStopping bot...")
            break

        except Exception as e:
            log_error("runner", "loop_error", str(e))
            print("Error occurred")


# -----------------------------
# Entry Point
# -----------------------------
if __name__ == "__main__":
    run_mock_bot()
