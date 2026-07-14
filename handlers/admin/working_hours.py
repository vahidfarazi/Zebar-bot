"""
handlers/admin/working_hours.py

Manage system working hours.
"""

from database.settings import (
    get_setting,
    set_setting,
)


DEFAULT_START = "07:00"
DEFAULT_END = "13:00"


# -------------------------------------------------
# Show Working Hours
# -------------------------------------------------
def show_working_hours():

    start = get_setting(
        "WORK_START",
    ) or DEFAULT_START

    end = get_setting(
        "WORK_END",
    ) or DEFAULT_END

    return {

        "text": (
            "🕒 ساعات کاری سامانه\n\n"
            f"شروع فعالیت: {start}\n"
            f"پایان فعالیت: {end}\n\n"
            "در این بازه امکان ثبت درخواست فعال است."
        ),

        "keyboard": [

            ["✏️ تغییر ساعات کاری"],

            ["🏠 بازگشت"],

        ],

    }


# -------------------------------------------------
# Update Working Hours
# -------------------------------------------------
def update_working_hours(
    start: str,
    end: str,
):

    set_setting(
        "WORK_START",
        start,
    )

    set_setting(
        "WORK_END",
        end,
    )

    return {

        "text":
            "✅ ساعات کاری با موفقیت تغییر کرد.",

    }
