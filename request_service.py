"""
request_service.py

Request creation service.
"""

from database import (
    insert_request,
    get_last_tracking_number,
)

from ticket_formatter import (
    format_database,
    format_expert,
    format_success,
)

from logger import log_info


# -----------------------------
# Generate Tracking Code
# -----------------------------
def generate_tracking_code() -> str:

    last = get_last_tracking_number()

    if last is None:
        return "SR-2026-0000001"

    number = int(
        last.split("-")[-1]
    ) + 1

    return f"SR-2026-{number:07d}"


# -----------------------------
# Create Request
# -----------------------------
def create_request(
    chat_id: int,
    data: dict,
) -> dict:
    """
    Creates request and returns result.
    """

    tracking = generate_tracking_code()

    description = format_database(
        data,
    )

    insert_request(

        tracking_code=tracking,

        chat_id=chat_id,

        title=data.get(
            "sub_service",
            data.get("service"),
        ),

        description=description,

    )

    # -------- Expert Message --------

    expert_message = format_expert(

        tracking,

        chat_id,

        data,

    )

    # TODO
    # send_to_expert_group(expert_message)

    log_info(

        "request_service",

        "create_request",

        tracking,

    )

    return {

        "tracking": tracking,

        "expert_message": expert_message,

        "user_message": format_success(
            tracking,
        ),

    }
