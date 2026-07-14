"""
database/dashboard.py

Dashboard statistics repository.
"""

from .crud import (
    fetch_one,
    fetch_all,
)


# =================================================
# General Statistics
# =================================================

def get_dashboard_summary() -> dict:
    """
    Main dashboard counters.
    """

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
                    WHEN status='PENDING'
                    THEN 1
                END
            ) AS pending,

            COUNT(
                CASE
                    WHEN status='CLOSED'
                    THEN 1
                END
            ) AS closed

        FROM requests
        """
    )

    if not row:

        return {
            "total": 0,
            "open": 0,
            "pending": 0,
            "closed": 0,
        }


    return {

        "total": row["total"] or 0,

        "open": row["open"] or 0,

        "pending": row["pending"] or 0,

        "closed": row["closed"] or 0,

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
# Daily Statistics
# =================================================

def get_daily_statistics(
    limit: int = 30,
) -> list[dict]:
    """
    Daily request count.
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
# Expert Performance
# =================================================

def get_expert_statistics() -> list[dict]:
    """
    Expert response statistics.
    """

    rows = fetch_all(
        """
        SELECT

            expert_id,

            COUNT(*) AS total

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
    Recent requests for admin panel.
    """

    rows = fetch_all(
        """
        SELECT

            id,

            tracking_code,

            chat_id,

            service,

            status,

            created_at

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
    SLA metrics.
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
