"""
database/tracking_sequence.py

Tracking sequence repository.
"""

from .crud import (
    execute,
    fetch_one,
)


# ----------------------------------------
# Get Next Tracking Number
# ----------------------------------------
def get_next_tracking_number(
    year: str,
    department_code: str,
) -> int:
    """
    Returns next sequence number.
    """

    row = fetch_one(
        """
        SELECT last_number
        FROM tracking_sequences
        WHERE year = %s
        AND department_code = %s
        """,
        (
            year,
            department_code,
        ),
    )

    # First record
    if row is None:

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
                1
            )
            """,
            (
                year,
                department_code,
            ),
        )

        return 1

    next_number = row["last_number"] + 1

    execute(
        """
        UPDATE tracking_sequences
        SET last_number = %s
        WHERE year = %s
        AND department_code = %s
        """,
        (
            next_number,
            year,
            department_code,
        ),
    )

    return next_number
