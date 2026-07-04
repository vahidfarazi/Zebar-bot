"""
request_service.py

Core business logic for service request lifecycle.
Handles creation, update, closure, and tracking.
"""

from database import get_connection
from tracking import generate_tracking_code
from logger import log_info, log_error


# -----------------------------
# Create Request
# -----------------------------
def create_request(chat_id: int, service: str, sub_service: str = None, priority: str = "NORMAL") -> str:
    """
    Create a new service request and return tracking code.
    """

    try:
        conn = get_connection()
        cursor = conn.cursor()

        tracking_code = generate_tracking_code()

        cursor.execute(
            """
            INSERT INTO requests (
                tracking_code,
                chat_id,
                service,
                sub_service,
                status,
                priority
            )
            VALUES (?, ?, ?, ?, 'NEW', ?)
            """,
            (tracking_code, chat_id, service, sub_service, priority)
        )

        conn.commit()
        conn.close()

        log_info("request_service", f"REQUEST_CREATED: {tracking_code}")

        return tracking_code

    except Exception as e:
        log_error("request_service", f"CREATE_REQUEST_FAILED: {e}")
        return None


# -----------------------------
# Get Request by Tracking
# -----------------------------
def get_request(tracking_code: str):
    """
    Retrieve request details by tracking code.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM requests WHERE tracking_code = ?",
        (tracking_code,)
    )

    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return dict(row)


# -----------------------------
# Close Request
# -----------------------------
def close_request(tracking_code: str) -> bool:
    """
    Close a service request.
    """

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE requests
            SET status = 'CLOSED',
                updated_at = CURRENT_TIMESTAMP
            WHERE tracking_code = ?
            """,
            (tracking_code,)
        )

        conn.commit()
        conn.close()

        log_info("request_service", f"REQUEST_CLOSED: {tracking_code}")

        return True

    except Exception as e:
        log_error("request_service", f"CLOSE_REQUEST_FAILED: {e}")
        return False


# -----------------------------
# Update Status
# -----------------------------
def update_request_status(tracking_code: str, status: str) -> bool:
    """
    Update request status.
    """

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE requests
            SET status = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE tracking_code = ?
            """,
            (status, tracking_code)
        )

        conn.commit()
        conn.close()

        log_info("request_service", f"STATUS_UPDATED: {tracking_code} -> {status}")

        return True

    except Exception as e:
        log_error("request_service", f"UPDATE_STATUS_FAILED: {e}")
        return False
