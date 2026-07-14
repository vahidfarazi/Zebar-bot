"""
database/reports.py

Reporting queries for admin panel.
"""

from .crud import (
    fetch_one,
    fetch_all,
)


# =================================================
# Helper
# =================================================

def normalize_statistics(row: dict | None) -> dict:

    if not row:

        return {

            "total": 0,

            "open": 0,

            "closed": 0,

            "pending": 0,

            "transferred": 0,

        }

    return {

        "total": row.get("total") or 0,

        "open": row.get("open") or 0,

        "closed": row.get("closed") or 0,

        "pending": row.get("pending") or 0,

        "transferred": row.get("transferred") or 0,

    }


# =================================================
# Daily Statistics
# =================================================

def get_daily_statistics() -> dict:
    """
    Today's statistics.
    """

    row = fetch_one(
        """
        SELECT

            COUNT(*) AS total,

            SUM(
                CASE
                    WHEN status='OPEN'
                    THEN 1 ELSE 0
                END
            ) AS open,

            SUM(
                CASE
                    WHEN status='CLOSED'
                    THEN 1 ELSE 0
                END
            ) AS closed,

            SUM(
                CASE
                    WHEN status='PENDING'
                    THEN 1 ELSE 0
                END
            ) AS pending,

            SUM(
                CASE
                    WHEN expert_id IS NOT NULL
                    THEN 1 ELSE 0
                END
            ) AS transferred

        FROM requests

        WHERE DATE(created_at)=CURRENT_DATE
        """
    )

    return normalize_statistics(row)


# =================================================
# Weekly Statistics
# =================================================

def get_weekly_statistics() -> dict:
    """
    Last 7 days statistics.
    """

    row = fetch_one(
        """
        SELECT

            COUNT(*) AS total,

            SUM(
                CASE
                    WHEN status='OPEN'
                    THEN 1 ELSE 0
                END
            ) AS open,

            SUM(
                CASE
                    WHEN status='CLOSED'
                    THEN 1 ELSE 0
                END
            ) AS closed,

            SUM(
                CASE
                    WHEN status='PENDING'
                    THEN 1 ELSE 0
                END
            ) AS pending,

            SUM(
                CASE
                    WHEN expert_id IS NOT NULL
                    THEN 1 ELSE 0
                END
            ) AS transferred

        FROM requests

        WHERE created_at >= CURRENT_DATE - INTERVAL '6 days'
        """
    )

    return normalize_statistics(row)


# =================================================
# Monthly Statistics
# =================================================

def get_monthly_statistics() -> dict:
    """
    Last 30 days statistics.
    """

    row = fetch_one(
        """
        SELECT

            COUNT(*) AS total,

            SUM(
                CASE
                    WHEN status='OPEN'
                    THEN 1 ELSE 0
                END
            ) AS open,

            SUM(
                CASE
                    WHEN status='CLOSED'
                    THEN 1 ELSE 0
                END
            ) AS closed,

            SUM(
                CASE
                    WHEN status='PENDING'
                    THEN 1 ELSE 0
                END
            ) AS pending,

            SUM(
                CASE
                    WHEN expert_id IS NOT NULL
                    THEN 1 ELSE 0
                END
            ) AS transferred

        FROM requests

        WHERE created_at >= CURRENT_DATE - INTERVAL '29 days'
        """
    )

    return normalize_statistics(row)


# =================================================
# Chart Data - Daily
# =================================================

def get_daily_chart_data() -> list[dict]:
    """
    Data for dashboard charts.
    """

    rows = fetch_all(
        """
        SELECT

            DATE(created_at) AS date,

            COUNT(*) AS total

        FROM requests

        WHERE created_at >= CURRENT_DATE - INTERVAL '6 days'

        GROUP BY DATE(created_at)

        ORDER BY DATE(created_at)
        """
    )

    return [

        {

            "date": row["date"],

            "total": row["total"] or 0,

        }

        for row in rows

    ]


# =================================================
# Service Statistics
# =================================================

def get_service_statistics() -> list[dict]:
    """
    Requests grouped by service.
    """

    rows = fetch_all(
        """
        SELECT

            service,

            COUNT(*) AS total

        FROM requests

        GROUP BY service

        ORDER BY total DESC
        """
    )

    return [

        {

            "service": row["service"],

            "total": row["total"] or 0,

        }

        for row in rows

    ]


# =================================================
# Expert Performance
# =================================================

def get_expert_statistics() -> list[dict]:
    """
    Expert workload report.
    """

    rows = fetch_all(
        """
        SELECT

            e.chat_id,

            e.name,

            COUNT(r.id) AS total,

            SUM(
                CASE
                    WHEN r.status='CLOSED'
                    THEN 1 ELSE 0
                END
            ) AS closed

        FROM experts e

        LEFT JOIN requests r

        ON r.expert_id=e.chat_id

        GROUP BY e.chat_id,e.name

        ORDER BY total DESC
        """
    )

    return [

        {

            "chat_id": row["chat_id"],

            "name": row["name"],

            "total": row["total"] or 0,

            "closed": row["closed"] or 0,

        }

        for row in rows

    ]


# =================================================
# Full Dashboard Report
# =================================================

def get_dashboard_report() -> dict:
    """
    Complete dashboard data.
    """

    return {

        "daily":
            get_daily_statistics(),

        "weekly":
            get_weekly_statistics(),

        "monthly":
            get_monthly_statistics(),

        "chart":
            get_daily_chart_data(),

        "services":
            get_service_statistics(),

        "experts":
            get_expert_statistics(),

    }
