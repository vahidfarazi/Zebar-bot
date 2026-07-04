"""
request_service.py

Business logic for service requests.
Responsible for creating, updating, closing and managing requests.

NO SQL outside database.py.
NO user message formatting here.
"""

from datetime import datetime
from typing import Optional, Dict, Any

from database import execute, fetch_one
from tracking import generate_tracking_code
from logger import log_info, log_error
from working_hours import can_create_request


# -----------------------------
# Create Request
# -----------------------------
def create_request(
    chat_id: int,
    service: str,
    sub_service: str,
    priority: str = "NORMAL",
) -> Optional[str]:
    """
    Create a new service request and return tracking code.
    """

    try:
        if not can_create_request():
            return None

        tracking_code = generate_tracking_code()

        now = datetime.now().isoformat()

        execute(
            """
            INSERT INTO requests (
                tracking_code,
                chat_id,
                service,
                sub_service,
                status,
                priority,
                created_at,
                updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                tracking_code,
                chat_id,
                service,
                sub_service,
                "NEW",
                priority,
                now,
                now,
            ),
        )

        log_info(
            "request_service",
            "create_request",
            f"tracking={tracking_code}",
            user_id=chat_id,
        )

        return tracking_code

    except Exception as e:
        log_error("request_service", "create_request_failed", str(e), user_id=chat_id)
        return None


# -----------------------------
# Close Request
# -----------------------------
def close_request(tracking_code: str, closed_by: str = "SYSTEM") -> bool:
    """
    Close a request.
    """

    try:
        request = fetch_one(
            "SELECT * FROM requests WHERE tracking_code = ?",
            (tracking_code,),
        )

        if not request:
            return False

        execute(
            """
            UPDATE requests
            SET status = ?, closed_at = ?, updated_at = ?
            WHERE tracking_code = ?
            """,
            (
                "CLOSED",
                datetime.now().isoformat(),
                datetime.now().isoformat(),
                tracking_code,
            ),
        )

        log_info(
            "request_service",
            "close_request",
            f"tracking={tracking_code}, by={closed_by}",
            user_id=request["chat_id"],
        )

        return True

    except Exception as e:
        log_error("request_service", "close_request_failed", str(e))
        return False


# -----------------------------
# Get Request
# -----------------------------
def get_request(tracking_code: str) -> Optional[Dict[str, Any]]:
    """
    Fetch request details.
    """

    try:
        return fetch_one(
            "SELECT * FROM requests WHERE tracking_code = ?",
            (tracking_code,),
        )

    except Exception as e:
        log_error("request_service", "get_request_failed", str(e))
        return None


# -----------------------------
# Update Status
# -----------------------------
def update_status(tracking_code: str, status: str) -> bool:
    """
    Update request status.
    """

    try:
        execute(
            """
            UPDATE requests
            SET status = ?, updated_at = ?
            WHERE tracking_code = ?
            """,
            (
                status,
                datetime.now().isoformat(),
                tracking_code,
            ),
        )

        log_info(
            "request_service",
            "update_status",
            f"tracking={tracking_code}, status={status}",
        )

        return True

    except Exception as e:
        log_error("request_service", "update_status_failed", str(e))
        return False
