import sqlite3
import jdatetime

DB_NAME = "azarakhsh.db"

PREFIX = "SR"


def get_persian_year():
    """
    سال شمسی جاری
    """
    return str(jdatetime.date.today().year)


def generate_tracking_code():

    conn = sqlite3.connect(DB_NAME)

    cur = conn.cursor()

    year = get_persian_year()

    cur.execute(
        """
        SELECT tracking_code
        FROM requests
        WHERE tracking_code LIKE ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (f"{PREFIX}-{year}-%",)
    )

    row = cur.fetchone()

    if row is None:

        number = 1

    else:

        try:

            number = int(row[0].split("-")[-1]) + 1

        except:

            number = 1

    conn.close()

    return f"{PREFIX}-{year}-{number:07d}"
