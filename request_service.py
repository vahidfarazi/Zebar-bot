"""
request_service.py

Request creation service.
"""

from database import (
    insert_request,
    get_last_tracking_number,
    add_message,
)

from ticket_formatter import (
    format_expert,
    format_success,
)

from notification_service import (
    notify_experts,
)

from logger import (
    log_info,
)


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
    Create new request.
    """

    tracking = generate_tracking_code()

    # -----------------------------
    # Save Request
    # -----------------------------
    insert_request(

        tracking_code=tracking,

        chat_id=chat_id,

        service=data["service"],

        sub_service=data.get(
            "sub_service",
        ),

    )

    # -----------------------------
    # Save First Message
    # -----------------------------
    add_message(

        tracking_code=tracking,

        sender_type="USER",

        sender_id=chat_id,

        message_type="REQUEST",

        message=format_expert(
            tracking,
            chat_id,
            data,
        ),

    )

    # -----------------------------
    # Expert Message
    # -----------------------------
    expert_message = format_expert(

        tracking,

        chat_id,

        data,

    )

    notify_experts(
        expert_message,
    )

    log_info(

        "request_service",

        "create_request",

        tracking,

    )

    return {

        "tracking": tracking,

        "user_message": format_success(
            tracking,
        ),

    }
