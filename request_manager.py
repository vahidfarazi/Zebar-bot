import sqlite3

from tracking import generate_tracking_code

DB_NAME = "azarakhsh.db"


def create_request(
    chat_id,
    service,
    sub_service,
    identifier_type,
    identifier_value
):

    tracking = generate_tracking_code()

    conn = sqlite3.connect(DB_NAME)

    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO requests(

            tracking_code,

            chat_id,

            service,

            sub_service,

            identifier_type,

            identifier_value,

            status

        )

        VALUES(?,?,?,?,?,?,?)

        """,

        (

            tracking,

            chat_id,

            service,

            sub_service,

            identifier_type,

            identifier_value,

            "در انتظار بررسی"

        )

    )

    conn.commit()

    conn.close()

    return tracking
