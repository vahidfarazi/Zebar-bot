"""
request_service.py

Request creation service.
"""

from datetime import datetime

from database import (
    insert_request,
    add_message,
    get_next_tracking_number,
)

from ticket_formatter import (
    format_request,
    format_expert,
    format_success,
)

from notification_service import (
    notify_experts,
)

from logger import (
    log_info,
    log_error,
)


# ----------------------------------------
# Jalali Year (Temporary)
# ----------------------------------------
def get_current_jalali_year() -> str:
    """
    Temporary mapping.

    2026 -> 1405

    Later this will use jdatetime.
    """

    year = datetime.now().year

    return str(year - 621)


# ----------------------------------------
# Department Code
# ----------------------------------------
def get_department_code(
    service: str,
) -> str:
    """
    Department codes.

    11 = Customer Service
    22 = Safety
    33 = Engineering

    Currently every request belongs to
    Customer Service.
    """

    return "11"


# ----------------------------------------
# Generate Tracking Code
# ----------------------------------------
def generate_tracking_code(
    service: str,
) -> str:

    year = get_current_jalali_year()

    department = get_department_code(
        service,
    )

    number = get_next_tracking_number(
        year,
        department,
    )

    return (
        f"{year}"
        f"{department}"
        f"{number:07d}"
    )


# ----------------------------------------
# Create Request
# ----------------------------------------
def create_request(
    chat_id: int,
    data: dict,
) -> dict:
    """
    Create new request.
    """

    try:

        tracking = generate_tracking_code(
            data["service"],
        )

        # -------------------------
        # Save Request
        # -------------------------

        insert_request(

            tracking_code=tracking,

            chat_id=chat_id,

            service=data["service"],

            sub_service=data.get(
                "sub_service",
            ),

        )

        # -------------------------
        # Save First User Message
        # -------------------------

        add_message(

            tracking_code=tracking,

            sender_type="USER",

            sender_id=chat_id,

            message_type="REQUEST",

            message=format_request(
                data,
            ),

        )

        # -------------------------
        # Expert Notification
        # -------------------------

        expert_message = format_expert(

            tracking,

            chat_id,

            data,

        )

        notify_experts(

            tracking,

            expert_message,

        )

        log_info(

            "request_service",

            "create_request",

            tracking,

        )

        # -------------------------
        # Result
        # -------------------------

        return {

            "tracking": tracking,

            "user_message": format_success(
                tracking,
            ),

        }

    except Exception as e:

        log_error(

            "request_service",

            "create_request",

            str(e),

        )

        raise
