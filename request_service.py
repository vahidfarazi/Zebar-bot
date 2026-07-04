from datetime import datetime

from database import (
    request_exists,
    create_request,
    get_request_by_tracking,
    add_request_message,
)

from tracking import generate_tracking_code


def register_request(

    chat_id,

    service,

    sub_service,

    identifier_type,

    identifier_value

):

    old = request_exists(
        service,
        identifier_value
    )

    if old:

        return {

            "success": False,

            "message": "duplicate",

            "tracking_code": old["tracking_code"]

        }

    tracking_code = generate_tracking_code()

    request_id = create_request(

        tracking_code,

        chat_id,

        service,

        sub_service,

        identifier_type,

        identifier_value

    )

    add_request_message(

        request_id=request_id,

        sender_type="SYSTEM",

        sender_id=0,

        message="درخواست با موفقیت ثبت شد."

    )

    return {

        "success": True,

        "tracking_code": tracking_code,

        "request_id": request_id

    }


def get_request(tracking_code):

    return get_request_by_tracking(tracking_code)
