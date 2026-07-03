import sqlite3
from datetime import datetime

DB_NAME = "azarakhsh.db"


def get_persian_year():
    """
    فعلاً سال را ثابت گذاشته‌ایم.
    بعداً به صورت خودکار از تاریخ شمسی محاسبه می‌شود.
    """
    return "1405"


def generate_tracking_code():

    conn = sqlite3.connect(DB_NAME)

    cur = conn.cursor()

    year = get_persian_year()

    cur.execute(
        """
        SELECT COUNT(*)
        FROM requests
        WHERE tracking_code LIKE ?
        """,
        (f"SR-{year}-%",)
    )

    count = cur.fetchone()[0] + 1

    tracking_code = f"SR-{year}-{count:07d}"

    conn.close()

    return tracking_code
