"""
database/statistics.py

Dashboard statistics repository.
"""

from .crud import fetch_one, fetch_all


# -------------------------------------------------
# Dashboard Statistics
# -------------------------------------------------
def get_dashboard_statistics() -> dict:

    row = fetch_one(
        """
        SELECT

        COUNT(*) FILTER(
            WHERE status = 'OPEN'
        ) AS open,

        COUNT(*) FILTER(
            WHERE status = 'CLOSED'
        ) AS closed,

        COUNT(*) FILTER(
            WHERE DATE(created_at)=CURRENT_DATE
        ) AS today

        FROM requests
        """
    )

    expert = fetch_one(
        """
        SELECT COUNT(*) AS total

        FROM experts

        WHERE is_active=TRUE
        """
    )

    return {

        "open":
            row["open"] or 0,

        "closed":
            row["closed"] or 0,

        "today":
            row["today"] or 0,

        "experts":
            expert["total"] or 0,

    }


# -------------------------------------------------
# Daily Statistics
# -------------------------------------------------
def get_daily_statistics() -> dict:

    row = fetch_one(
        """
        SELECT

        COUNT(*) AS total,

        COUNT(*) FILTER(
            WHERE status='OPEN'
        ) AS open,

        COUNT(*) FILTER(
            WHERE status='CLOSED'
        ) AS closed

        FROM requests

        WHERE DATE(created_at)=CURRENT_DATE
        """
    )

    return dict(row)


# -------------------------------------------------
# Weekly Statistics
# -------------------------------------------------
def get_weekly_statistics() -> dict:

    row = fetch_one(
        """
        SELECT

        COUNT(*) AS total,

        COUNT(*) FILTER(
            WHERE status='OPEN'
        ) AS open,

        COUNT(*) FILTER(
            WHERE status='CLOSED'
        ) AS closed

        FROM requests

        WHERE created_at >= CURRENT_DATE - INTERVAL '7 days'
        """
    )

    return dict(row)


# -------------------------------------------------
# Monthly Statistics
# -------------------------------------------------
def get_monthly_statistics() -> dict:

    row = fetch_one(
        """
        SELECT

        COUNT(*) AS total,

        COUNT(*) FILTER(
            WHERE status='OPEN'
        ) AS open,

        COUNT(*) FILTER(
            WHERE status='CLOSED'
        ) AS closed

        FROM requests

        WHERE created_at >= CURRENT_DATE - INTERVAL '30 days'
        """
    )

    return dict(row)


# -------------------------------------------------
# Service Statistics (For Charts)
# -------------------------------------------------
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

# -------------------------------------------------
# Expert Performance
# -------------------------------------------------
def get_expert_statistics() -> list[dict]:

    rows = fetch_all(
        """
        SELECT

        e.chat_id,

        e.name,

        COUNT(r.id) AS total

        FROM experts e

        LEFT JOIN requests r

        ON r.expert_id = e.chat_id

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


# -------------------------------------------------
# Daily Chart Data
# -------------------------------------------------
def get_daily_chart_data(
    days: int = 7,
) -> list[dict]:

    rows = fetch_all(
        """
        SELECT

        DATE(created_at) AS day,

        COUNT(*) AS total

        FROM requests

        WHERE created_at >= CURRENT_DATE - (%s * INTERVAL '1 day')

        GROUP BY DATE(created_at)

        ORDER BY day
        """,
        (
            days,
        ),
    )

    return [
        dict(row)
        for row in rows
    ]
