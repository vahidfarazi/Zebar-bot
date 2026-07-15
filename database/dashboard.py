"""
database/dashboard.py

Dashboard statistics repository.
"""

from .crud import (
    fetch_one,
    fetch_all,
)


# =================================================
# Dashboard Statistics
# =================================================

def get_dashboard_statistics() -> dict:
    """
    Main dashboard counters.
    """

    row = fetch_one(
        """
        SELECT

            COUNT(*) AS total,

            COUNT(
                CASE
                    WHEN status = 'OPEN'
                    THEN 1
                END
            ) AS open,

            COUNT(
                CASE
                    WHEN status = 'PENDING'
                    THEN 1
                END
            ) AS pending,

            COUNT(
                CASE
                    WHEN status = 'CLOSED'
                    THEN 1
                END
            ) AS closed,

            COUNT(
                CASE
                    WHEN expert_id IS NOT NULL
                    THEN 1
                END
            ) AS transferred

        FROM requests
        """
    )

    if not row:

        return {

            "total": 0,

            "open": 0,

            "pending": 0,

            "closed": 0,

            "transferred": 0,

        }

    return {

        "total":
            row["total"] or 0,

        "open":
            row["open"] or 0,

        "pending":
            row["pending"] or 0,

        "closed":
            row["closed"] or 0,

        "transferred":
            row["transferred"] or 0,

    }


# =================================================
# Complete Dashboard
# =================================================

def get_dashboard() -> dict:
    """
    Complete dashboard data.
    """

    return {

        "statistics":
            get_dashboard_statistics(),

        "services":
            get_service_statistics(),

        "experts":
            get_expert_statistics(),

        "recent":
            get_recent_activity(),

        "sla":
            get_sla_dashboard(),

        "chart":
            get_daily_chart_data(),

    }

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

        dict(row)

        for row in rows

    ]


# =================================================
# Daily Chart Data
# =================================================

def get_daily_chart_data(
    limit: int = 30,
) -> list[dict]:
    """
    Daily request chart data.
    """

    rows = fetch_all(
        """
        SELECT

            DATE(created_at) AS day,

            COUNT(*) AS total

        FROM requests

        GROUP BY DATE(created_at)

        ORDER BY day DESC

        LIMIT %s
        """,
        (
            limit,
        ),
    )

    return [

        dict(row)

        for row in rows

    ]

# =================================================
# Expert Statistics
# =================================================

def get_expert_statistics() -> list[dict]:
    """
    Expert workload statistics.
    """

    rows = fetch_all(
        """
        SELECT

            expert_id,

            COUNT(*) AS total,

            COUNT(
                CASE
                    WHEN status = 'CLOSED'
                    THEN 1
                END
            ) AS closed

        FROM requests

        WHERE expert_id IS NOT NULL

        GROUP BY expert_id

        ORDER BY total DESC
        """
    )

    return [

        dict(row)

        for row in rows

    ]


# =================================================
# Recent Activity
# =================================================

def get_recent_activity(
    limit: int = 20,
) -> list[dict]:
    """
    Recent requests.
    """

    rows = fetch_all(
        """
        SELECT

            id,

            tracking_code,

            chat_id,

            service,

            status,

            created_at,

            updated_at

        FROM requests

        ORDER BY id DESC

        LIMIT %s
        """,
        (
            limit,
        ),
    )

    return [

        dict(row)

        for row in rows

    ]

# =================================================
# SLA Dashboard
# =================================================

def get_sla_dashboard() -> dict:
    """
    SLA response and close metrics.
    """

    row = fetch_one(
        """
        SELECT

            AVG(
                EXTRACT(
                    EPOCH FROM
                    (
                        first_response_at
                        -
                        created_at
                    )
                ) / 60
            ) AS response_time,

            AVG(
                EXTRACT(
                    EPOCH FROM
                    (
                        closed_at
                        -
                        created_at
                    )
                ) / 60
            ) AS close_time

        FROM requests
        """
    )

    if not row:

        return {

            "response_time": 0,

            "close_time": 0,

        }

    return {

        "response_time":
            round(
                row["response_time"] or 0,
                2,
            ),

        "close_time":
            round(
                row["close_time"] or 0,
                2,
            ),

    }


# =================================================
# Backward Compatibility
# =================================================

def get_dashboard_summary() -> dict:
    """
    Backward compatibility.
    """

    return get_dashboard_statistics()
