"""
handlers/admin/holidays.py

Manage system holidays.
"""

from database.holidays import (
    add_holiday,
    remove_holiday,
    get_holidays,
)

from menus import ADMIN_MENU


# -------------------------------------------------
# Show Holidays
# -------------------------------------------------
def holidays_menu():

    holidays = get_holidays()

    if not holidays:

        text = (
            "📅 تعطیلات ثبت شده‌ای وجود ندارد."
        )

    else:

        text = "📅 تعطیلات سامانه\n\n"

        for item in holidays:

            text += (
                f"📌 {item['holiday_date']}\n"
            )

    return {

        "text": text,

        "keyboard": [

            ["➕ افزودن تعطیلی"],

            ["➖ حذف تعطیلی"],

            ["🏠 بازگشت"],

        ],

    }


# -------------------------------------------------
# Add Holiday
# -------------------------------------------------
def create_holiday(
    date: str,
):

    add_holiday(
        date,
    )

    return {

        "text":
            "✅ تعطیلی ثبت شد.",

        "keyboard":
            ADMIN_MENU,

    }


# -------------------------------------------------
# Delete Holiday
# -------------------------------------------------
def delete_holiday(
    date: str,
):

    remove_holiday(
        date,
    )

    return {

        "text":
            "✅ تعطیلی حذف شد.",

        "keyboard":
            ADMIN_MENU,

    }
