"""
calendar_utils.py

Jalali calendar keyboard generator
for Bale admin panel.
"""


from date_utils import (
    get_jalali_calendar,
    current_jalali_month,
    previous_jalali_month,
    next_jalali_month,
)



# ==========================================
# Month Name
# ==========================================

JALALI_MONTH_NAMES = {

    1: "فروردین",
    2: "اردیبهشت",
    3: "خرداد",
    4: "تیر",
    5: "مرداد",
    6: "شهریور",
    7: "مهر",
    8: "آبان",
    9: "آذر",
    10: "دی",
    11: "بهمن",
    12: "اسفند",

}



# ==========================================
# Calendar Keyboard
# ==========================================

def build_calendar_keyboard(
    year: int,
    month: int,
) -> list[list[str]]:


    keyboard = []


    # Header

    keyboard.append(

        [
            f"{JALALI_MONTH_NAMES[month]} {year}"

        ]

    )



    # Navigation

    prev_year, prev_month = previous_jalali_month(

        year,

        month,

    )


    next_year, next_month = next_jalali_month(

        year,

        month,

    )


    keyboard.append(

        [

            f"⬅️ {prev_month}/{prev_year}",

            "امروز",

            f"➡️ {next_month}/{next_year}",

        ]

    )



    # Week days

    keyboard.append(

        [

            "ش",

            "ی",

            "د",

            "س",

            "چ",

            "پ",

            "ج",

        ]

    )



    # Days

    calendar = get_jalali_calendar(

        year,

        month,

    )



    for week in calendar:


        row = []


        for day in week:


            if day:

                row.append(

                    f"{year}/{str(month).zfill(2)}/{str(day).zfill(2)}"

                )

            else:

                row.append(
                    ""
                )


        keyboard.append(
            row
        )



    keyboard.append(

        [

            "❌ انصراف",

        ]

    )


    return keyboard



# ==========================================
# Open Current Calendar
# ==========================================

def open_calendar():

    year, month = current_jalali_month()


    return {

        "text":

            f"📅 انتخاب تاریخ\n\n"
            f"{JALALI_MONTH_NAMES[month]} {year}",


        "keyboard":

            build_calendar_keyboard(

                year,

                month,

            ),

              }
