"""
handlers/user/form_handler.py

Generic request form handler.
"""

from form_engine import FormEngine

from form_registry import get_form

from user_state import (
    get_data,
    update_data,
    set_state,
    reset,
)

from database import (
    insert_request,
    get_last_tracking_number,
)


def _next_tracking():

    last = get_last_tracking_number()

    if last is None:
        return "SR-2026-0000001"

    number = int(last.split("-")[-1]) + 1

    return f"SR-2026-{number:07d}"


def handle_form(
    chat_id: int,
    message: str,
    state: str,
):

    data = get_data(chat_id)

    service = data.get("service")

    form = get_form(service)

    engine = FormEngine(form)

    # -----------------------------
    # Validate
    # -----------------------------
    if not engine.validate(
        state,
        message,
    ):

        return {

            "text":
                f"{engine.title(state)} معتبر نیست.\n\n"
                f"لطفاً دوباره وارد کنید.",

        }

    # -----------------------------
    # Save Field
    # -----------------------------
    field = engine.field_name(state)

    update_data(
        chat_id,
        field,
        message,
    )

    # -----------------------------
    # Next Step
    # -----------------------------
    next_step = engine.next_step(state)

    if next_step:

        set_state(
            chat_id,
            next_step["state"],
        )

        return {

            "text":
                f"لطفاً {next_step['title']} را وارد کنید.",

        }

    # -----------------------------
    # Finish
    # -----------------------------
    tracking = _next_tracking()

    insert_request(

        tracking_code=tracking,

        chat_id=chat_id,

        title=data.get(
            "sub_service",
            service,
        ),

        description=str(
            get_data(chat_id)
        ),

    )

    reset(chat_id)

    return {

        "text":
            "✅ درخواست شما ثبت شد.\n\n"
            f"کد پیگیری:\n{tracking}",

    }
