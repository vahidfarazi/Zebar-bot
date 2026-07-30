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

# ==========================================
# Next Jalali Month
# ==========================================

def next_jalali_month(
    year: int,
    month: int,
) -> tuple[int, int]:

    if month == 12:

        return (
            year + 1,
            1,
        )

    return (
        year,
        month + 1,
    )


# ==========================================
# Jalali Month Range
# ==========================================

def jalali_month_range(
    year: int,
    month: int,
) -> tuple[str, str]:

    start = jalali_to_gregorian(
        f"{year}-{str(month).zfill(2)}-01",
    )

    next_year, next_month = next_jalali_month(
        year,
        month,
    )

    end = jalali_to_gregorian(
        f"{next_year}-{str(next_month).zfill(2)}-01",
    )

    return (
        start,
        end,
    )

# ==========================================
# Previous Jalali Day
# ==========================================

def previous_day(
    date_str: str,
) -> str:

    year, month, day = map(
        int,
        date_str.replace("-", "/").split("/"),
    )

    d = jdatetime.date(
        year,
        month,
        day,
    )

    d = d.fromgregorian(
        date=d.togregorian()
        - datetime.timedelta(days=1)
    )

    return d.strftime(
        "%Y/%m/%d",
    )


# ==========================================
# Next Jalali Day
# ==========================================

def next_day(
    date_str: str,
) -> str:

    year, month, day = map(
        int,
        date_str.replace("-", "/").split("/"),
    )

    d = jdatetime.date(
        year,
        month,
        day,
    )

    d = d.fromgregorian(
        date=d.togregorian()
        + datetime.timedelta(days=1)
    )

    return d.strftime(
        "%Y/%m/%d",
    )


# ==========================================
# Previous Month
# ==========================================

def previous_jalali_month(
    year: int,
    month: int,
) -> tuple[int, int]:

    if month == 1:

        return (
            year - 1,
            12,
        )

    return (
        year,
        month - 1,
    )


# ==========================================
# Previous Week
# ==========================================

def previous_week(
    date_str: str,
) -> str:

    year, month, day = map(
        int,
        date_str.replace("-", "/").split("/"),
    )

    d = jdatetime.date(
        year,
        month,
        day,
    )

    d = d.fromgregorian(
        date=d.togregorian()
        - datetime.timedelta(days=7)
    )

    return d.strftime(
        "%Y/%m/%d",
    )


# ==========================================
# Next Week
# ==========================================

def next_week(
    date_str: str,
) -> str:

    year, month, day = map(
        int,
        date_str.replace("-", "/").split("/"),
    )

    d = jdatetime.date(
        year,
        month,
        day,
    )

    d = d.fromgregorian(
        date=d.togregorian()
        + datetime.timedelta(days=7)
    )

    return d.strftime(
        "%Y/%m/%d",
    )
