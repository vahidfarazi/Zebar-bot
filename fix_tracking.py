from database import get_connection


def fix_tracking_sequence():

    conn = get_connection()

    try:
        with conn.cursor() as cursor:

            cursor.execute(
                """
                UPDATE tracking_sequences
                SET last_number = 10
                WHERE year='1405'
                AND department_code='11'
                """
            )

            conn.commit()

            print("### TRACKING FIX EXECUTED ###")

    finally:
        conn.close()
