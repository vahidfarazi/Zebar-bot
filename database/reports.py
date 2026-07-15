"""
database/reports.py

Reporting repository.
"""

from .crud import (
    fetch_one,
    fetch_all,
)


# =================================================
# Normalize
# =================================================

def normalize_statistics(
    row: dict | None,
) -> dict:

    if not row:

        return {
            "total": 0,
            "open": 0,
            "closed": 0,
            "pending": 0,
            "transferred": 0,
        }

    return {

        "total":
            row.get("total") or 0,

        "open":
            row.get("open") or 0,

        "closed":
            row.get("closed") or 0,

        "pending":
            row.get("pending") or 0,

        "transferred":
            row.get("transferred") or 0,

    }



# =================================================
# Period Statistics
# =================================================

def _get_period_statistics(
    days: int,
) -> dict:

    row = fetch_one(
        """
        SELECT

            COUNT(*) AS total,

            COUNT(
                CASE
                    WHEN status='OPEN'
                    THEN 1
                END
            ) AS open,

            COUNT(
                CASE
                    WHEN status='CLOSED'
                    THEN 1
                END
            ) AS closed,

            COUNT(
                CASE
                    WHEN status='PENDING'
                    THEN 1
                END
            ) AS pending,

            COUNT(
                CASE
                    WHEN expert_id IS NOT NULL
                    THEN 1
                END
            ) AS transferred

        FROM requests

        WHERE created_at >=
            CURRENT_DATE - (%s * INTERVAL '1 day')
        """,
        (
            days,
        ),
    )

    return normalize_statistics(
        row
    )



# =================================================
# Daily
# =================================================

def get_daily_statistics() -> dict:

    row = fetch_one(
        """
        SELECT

            COUNT(*) AS total,

            COUNT(
                CASE
                    WHEN status='OPEN'
                    THEN 1
                END
            ) AS open,

            COUNT(
                CASE
                    WHEN status='CLOSED'
                    THEN 1
                END
            ) AS closed,

            COUNT(
                CASE
                    WHEN status='PENDING'
                    THEN 1
                END
            ) AS pending,

            COUNT(
                CASE
                    WHEN expert_id IS NOT NULL
                    THEN 1
                END
            ) AS transferred

        FROM requests

        WHERE DATE(created_at)=CURRENT_DATE
        """
    )

    return normalize_statistics(
        row
    )



# =================================================
# Weekly
# =================================================

def get_weekly_statistics() -> dict:

    return _get_period_statistics(
        7
    )



# =================================================
# Monthly
# =================================================

def get_monthly_statistics() -> dict:

    return _get_period_statistics(
        30
    )



# =================================================
# Chart
# =================================================

def get_daily_chart_data(
    days: int = 7,
) -> list[dict]:

    rows = fetch_all(
        """
        SELECT

            DATE(created_at) AS date,

            COUNT(*) AS total

        FROM requests

        WHERE created_at >=
            CURRENT_DATE - (%s * INTERVAL '1 day')

        GROUP BY DATE(created_at)

        ORDER BY date
        """,
        (
            days,
        ),
    )

    return [

        {
            "date":
                str(row["date"]),

            "total":
                row["total"] or 0,
        }

        for row in rows

    ]



# =================================================
# Services
# =================================================

def get_service_statistics() -> list[dict]:

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
        dict(row)
        for row in rows
    ]



# =================================================
# Experts
# =================================================

def get_expert_statistics() -> list[dict]:

    rows = fetch_all(
        """
        SELECT

            e.chat_id,

            e.name,

            COUNT(r.id) AS total,

            COUNT(
                CASE
                    WHEN r.status='CLOSED'
                    THEN 1
                END
            ) AS closed

        FROM experts e

        LEFT JOIN requests r

        ON r.expert_id=e.chat_id

        GROUP BY

            e.chat_id,

            e.name

        ORDER BY total DESC
        """
    )

    return [
        dict(row)
        for row in rows
    ]



# =================================================
# Dashboard Report
# =================================================

def get_dashboard_report() -> dict:

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



# =================================================
# Compatibility
# =================================================

def get_reports() -> dict:

    return get_dashboard_report()
