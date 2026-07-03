from datetime import datetime

from database import (
    request_exists,
    create_request,
)

from tracking import generate_tracking_code


def register_request(

    chat_id,

    service,

    sub_service,

    identifier_type,

    identifier_value

):

    # جلوگیری از ثبت تکراری
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

    create_request(

        tracking_code,

        chat_id,

        service,

        sub_service,

        identifier_type,

        identifier_value

    )

    return {

        "success": True,

        "tracking_code": tracking_code

    }
