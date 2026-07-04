"""
expert_service.py

Business logic for experts:
- assign requests
- reply to requests
- close requests
- manage expert workflow

NO SQL outside database.py
NO UI logic
"""

from datetime import datetime
from typing import Optional

from database import execute, fetch_one
from logger import log_info, log_error
from working_hours import get_current_time


# -----------------------------
# Assign Request
# -----------------------------
def assign_request(tracking_code: str, expert_id: int) -> bool:
    """
    Assign a request to an expert.
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
            SET expert_id = ?, status = ?, updated_at = ?
            WHERE tracking_code = ?
            """,
            (
                expert_id,
                "ASSIGNED",
                datetime.now().isoformat(),
                tracking_code,
            ),
        )

        log_info(
            "expert_service",
            "assign_request",
            f"tracking={tracking_code}, expert={expert_id}",
            user_id=expert_id,
        )

        return True

    except Exception as e:
        log_error("expert_service", "assign_failed", str(e))
        return False


# -----------------------------
# Expert Reply
# -----------------------------
def reply_to_request(tracking_code: str, expert_id: int, message: str) -> bool:
    """
    Save expert reply (message system placeholder).
    """

    try:
        request = fetch_one(
            "SELECT * FROM requests WHERE tracking_code = ?",
            (tracking_code,),
        )

        if not request:
            return False

        # In real system, we would have request_messages table
        execute(
            """
            INSERT INTO logs (
                timestamp,
                level,
                module,
                user_id,
                action,
                description,
                log_type
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                datetime.now().isoformat(),
                "INFO",
                "expert_service",
                expert_id,
                "reply",
                f"tracking={tracking_code}, msg={message}",
                "EXPERT",
            ),
        )

        log_info(
            "expert_service",
            "reply_to_request",
            f"tracking={tracking_code}",
            user_id=expert_id,
        )

        return True

    except Exception as e:
        log_error("expert_service", "reply_failed", str(e))
        return False


# -----------------------------
# Close Request (Expert)
# -----------------------------
def close_request_by_expert(tracking_code: str, expert_id: int) -> bool:
    """
    Expert closes a request.
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
            "expert_service",
            "close_by_expert",
            f"tracking={tracking_code}",
            user_id=expert_id,
        )

        return True

    except Exception as e:
        log_error("expert_service", "close_failed", str(e))
        return False


# -----------------------------
# Get Expert Requests
# -----------------------------
def get_expert_requests(expert_id: int):
    """
    Get all requests assigned to an expert.
    """

    try:
        return fetch_one(
            "SELECT * FROM requests WHERE expert_id = ?",
            (expert_id,),
        )

    except Exception as e:
        log_error("expert_service", "get_expert_requests_failed", str(e))
        return None
