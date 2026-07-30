"""
date_utils.py

Persian date utilities.
"""

from datetime import datetime

import jdatetime


# ==========================================
# Jalali -> Gregorian
# ==========================================

def jalali_to_gregorian(
    date_str: str,
) -> str:

    date_str = date_str.replace("-", "/")

    year, month, day = map(
        int,
        date_str.split("/"),
    )

    g = jdatetime.date(
        year,
        month,
        day,
    ).togregorian()

    return g.strftime(
        "%Y-%m-%d",
    )


# ==========================================
# Gregorian -> Jalali
# ==========================================

def gregorian_to_jalali(
    value,
) -> str:

    if isinstance(
        value,
        str,
    ):

        value = datetime.fromisoformat(
            value,
        )

    j = jdatetime.datetime.fromgregorian(
        datetime=value,
    )

    return j.strftime(
        "%Y/%m/%d",
    )


# ==========================================
# Now Jalali
# ==========================================

def today_jalali() -> str:

    return jdatetime.date.today().strftime(
        "%Y/%m/%d",
    )
