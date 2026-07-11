"""
request_service.py

Request creation service.
"""

from database import (
    insert_request,
    add_message,
    add_history,
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


# -----------------------------
# Department Codes
# -----------------------------
DEPARTMENT_CODES = {

    # خدمات مشترکین
    "NEW_CONNECTION": "11",
    "AFTER_SALES": "11",
    "METER_TEST": "11",
    "BILL_INQUIRY": "11",

}


# -----------------------------
# Generate Tracking Code
# -----------------------------
def generate_tracking_code(
    service: str,
) -> str:

    year = "1405"

    department = DEPARTMENT_CODES.get(
        service,
        "11",
    )

    sequence = get_next_tracking_number(
        year,
        department,
    )

    return (
        f"{year}"
        f"{department}"
        f"{sequence:07d}"
    )


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
        # Save User Message
        # -------------------------

        request_text = format_request(data)

        if data.get("description"):
            request_text += (
                "\n\n"
                "📝 توضیحات تکمیلی:\n"
                f"{data['description']}"
            )

        add_message(
            tracking_code=tracking,
            sender_type="USER",
            sender_id=chat_id,
            message_type="REQUEST",
            message=request_text,
        )

        # -------------------------
        # Save History
        # -------------------------

        add_history(
            tracking_code=tracking,
            event_type="REQUEST_CREATED",
            actor_type="USER",
            actor_id=chat_id,
            description="درخواست ثبت شد",
        )

        # -------------------------
        # Notify Experts
        # -------------------------

        expert_message = format_expert(
            tracking,
            chat_id,
            data,
        )

        if data.get("description"):
            expert_message += (
                "\n\n"
                "📝 توضیحات تکمیلی:\n"
                f"{data['description']}"
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
