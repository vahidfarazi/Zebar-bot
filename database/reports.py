"""
database/reports.py

Reporting queries for admin panel.
"""

from .crud import fetch_one


# -----------------------------
# Daily Statistics
# -----------------------------
def get_daily_statistics():
    """
    Today's statistics.
    """

    row = fetch_one(
        """
        SELECT
            COUNT(*) AS total,
            SUM(CASE WHEN status='OPEN' THEN 1 ELSE 0 END) AS open,
            SUM(CASE WHEN status='CLOSED' THEN 1 ELSE 0 END) AS closed
        FROM requests
        WHERE DATE(created_at)=DATE('now','localtime')
        """
    )

    if not row:

        return {
            "total": 0,
            "open": 0,
            "closed": 0,
        }

    return {
        "total": row["total"] or 0,
        "open": row["open"] or 0,
        "closed": row["closed"] or 0,
    }


# -----------------------------
# Weekly Statistics
# -----------------------------
def get_weekly_statistics():

    row = fetch_one(
        """
        SELECT
            COUNT(*) AS total,
            SUM(CASE WHEN status='OPEN' THEN 1 ELSE 0 END) AS open,
            SUM(CASE WHEN status='CLOSED' THEN 1 ELSE 0 END) AS closed
        FROM requests
        WHERE DATE(created_at)>=DATE('now','-6 day','localtime')
        """
    )

    if not row:

        return {
            "total": 0,
            "open": 0,
            "closed": 0,
        }

    return {
        "total": row["total"] or 0,
        "open": row["open"] or 0,
        "closed": row["closed"] or 0,
    }


# -----------------------------
# Monthly Statistics
# -----------------------------
def get_monthly_statistics():

    row = fetch_one(
        """
        SELECT
            COUNT(*) AS total,
            SUM(CASE WHEN status='OPEN' THEN 1 ELSE 0 END) AS open,
            SUM(CASE WHEN status='CLOSED' THEN 1 ELSE 0 END) AS closed
        FROM requests
        WHERE DATE(created_at)>=DATE('now','-29 day','localtime')
        """
    )

    if not row:

        return {
            "total": 0,
            "open": 0,
            "closed": 0,
        }

    return {
        "total": row["total"] or 0,
        "open": row["open"] or 0,
        "closed": row["closed"] or 0,
    }
