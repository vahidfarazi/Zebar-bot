"""
admin_service.py

Business logic for admin operations:
- expert management
- holiday management
- settings management
- request transfer
"""

from typing import Dict, Any
from database import get_connection
from logger import log_info, log_error


# -----------------------------
# Create Expert
# -----------------------------
def create_expert(chat_id: int, name: str, username: str, department: str) -> Dict[str, Any]:
    """
    Add new expert to system.
    """

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT OR REPLACE INTO experts (chat_id, name, username, department, is_active)
        VALUES (?, ?, ?, ?, 1)
        """, (chat_id, name, username, department))

        conn.commit()
        conn.close()

        log_info("admin_service", "create_expert", f"{chat_id}")

        return {"success": True}

    except Exception as e:
        log_error("admin_service", "create_expert", str(e))
        return {"success": False, "message": "خطا در ایجاد کارشناس"}


# -----------------------------
# Deactivate Expert
# -----------------------------
def deactivate_expert(chat_id: int) -> Dict[str, Any]:
    """
    Deactivate expert account.
    """

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE experts
        SET is_active = 0
        WHERE chat_id = ?
        """, (chat_id,))

        conn.commit()
        conn.close()

        log_info("admin_service", "deactivate_expert", f"{chat_id}")

        return {"success": True}

    except Exception as e:
        log_error("admin_service", "deactivate_expert", str(e))
        return {"success": False, "message": "خطا در غیرفعال‌سازی کارشناس"}


# -----------------------------
# Transfer Request
# -----------------------------
def transfer_request(request_id: int, expert_id: int) -> Dict[str, Any]:
    """
    Transfer request to another expert.
    """

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE requests
        SET expert_id = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """, (expert_id, request_id))

        conn.commit()
        conn.close()

        log_info("admin_service", "transfer_request", f"{request_id} -> {expert_id}")

        return {"success": True}

    except Exception as e:
        log_error("admin_service", "transfer_request", str(e))
        return {"success": False, "message": "خطا در انتقال درخواست"}


# -----------------------------
# Add Holiday
# -----------------------------
def add_holiday(date: str) -> Dict[str, Any]:
    """
    Add system holiday.
    """

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT OR IGNORE INTO holidays (holiday_date, enabled)
        VALUES (?, 1)
        """, (date,))

        conn.commit()
        conn.close()

        log_info("admin_service", "add_holiday", date)

        return {"success": True}

    except Exception as e:
        log_error("admin_service", "add_holiday", str(e))
        return {"success": False, "message": "خطا در ثبت تعطیلی"}


# -----------------------------
# Remove Holiday
# -----------------------------
def remove_holiday(date: str) -> Dict[str, Any]:
    """
    Remove system holiday.
    """

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        DELETE FROM holidays
        WHERE holiday_date = ?
        """, (date,))

        conn.commit()
        conn.close()

        log_info("admin_service", "remove_holiday", date)

        return {"success": True}

    except Exception as e:
        log_error("admin_service", "remove_holiday", str(e))
        return {"success": False, "message": "خطا در حذف تعطیلی"}


# -----------------------------
# Update Settings (MVP simple version)
# -----------------------------
def update_settings(key: str, value: str) -> Dict[str, Any]:
    """
    Update system settings.
    """

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO settings (key, value)
        VALUES (?, ?)
        ON CONFLICT(key) DO UPDATE SET value = excluded.value
        """, (key, value))

        conn.commit()
        conn.close()

        log_info("admin_service", "update_settings", f"{key}={value}")

        return {"success": True}

    except Exception as e:
        log_error("admin_service", "update_settings", str(e))
        return {"success": False, "message": "خطا در بروزرسانی تنظیمات"}
