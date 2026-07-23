"""
request_service.py

Request creation service.
"""

from database import (
    insert_request,
    add_message,
    add_history,
    get_next_tracking_number,
    get_request_by_tracking,
)

from ticket_formatter import (
    format_request,
    format_expert,
    format_success,
)

from notification_service import (
    notify_experts,
)

from working_hours import (
    can_create_request,
)

from logger import (
    log_info,
    log_error,
)


# =================================================
# Department Codes
# =================================================

DEPARTMENT_CODES = {

    "NEW_CONNECTION": "11",

    "AFTER_SALES": "11",

    "METER_TEST": "11",

    "BILL_INQUIRY": "11",

}



# =================================================
# Generate Tracking Code
# =================================================

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

    # تبدیل به عدد برای فرمت 7 رقمی
    try:
        sequence = int(sequence)
    except Exception:
        sequence = 1

    return (
        f"{year}"
        f"{department}"
        f"{sequence:07d}"
    )


# =================================================
# Create Request
# =================================================

def create_request(
    chat_id:int,
    data:dict,
) -> dict:


    try:


        # -----------------------------------------
        # Working Hours Check
        # -----------------------------------------

        if not can_create_request():

            return {

                "success":False,

                "user_message":
                    "⏰ در حال حاضر امکان ثبت درخواست وجود ندارد.",

            }



        service = data.get(
            "service",
        )


        if not service:

            return {

                "success":False,

                "user_message":
                    "❌ نوع خدمت مشخص نشده است.",

            }



        tracking = generate_tracking_code(

            service,

        )



        # -----------------------------------------
        # Save Request
        # -----------------------------------------

        insert_request(

            tracking_code=tracking,

            chat_id=chat_id,

            service=service,

            sub_service=data.get(
                "sub_service",
            ),

        )



        # -----------------------------------------
        # User Message
        # -----------------------------------------

        request_text = format_request(

            data,

        )



        add_message(

            tracking_code=tracking,

            sender_type="USER",

            sender_id=chat_id,

            message_type="REQUEST",

            message=request_text,

        )



        # -----------------------------------------
        # History
        # -----------------------------------------

        add_history(

            tracking_code=tracking,

            event_type="REQUEST_CREATED",

            actor_type="USER",

            actor_id=chat_id,

            description="درخواست جدید ثبت شد.",

        )



        # -----------------------------------------
        # Expert Notification
        # -----------------------------------------

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



        return {


            "success":True,


            "tracking":

                tracking,


            "user_message":

                format_success(

                    tracking,

                ),


        }



    except Exception as e:


        log_error(

            "request_service",

            "create_request",

            str(e),

        )


        return {


            "success":False,


            "user_message":

                "❌ خطا در ثبت درخواست. لطفاً دوباره تلاش کنید.",


        }
