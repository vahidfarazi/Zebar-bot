from database import execute


def fix_tracking_sequence():

    execute(
        """
        INSERT INTO tracking_sequences
        (
            year,
            department_code,
            last_number
        )
        VALUES
        (
            %s,
            %s,
            %s
        )
        ON CONFLICT (year, department_code)
        DO UPDATE SET
            last_number = EXCLUDED.last_number;
        """,
        (
            "1405",
            "11",
            10,
        ),
    )


    print("✅ Tracking sequence fixed")
