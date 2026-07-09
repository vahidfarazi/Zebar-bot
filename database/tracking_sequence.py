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
    Returns next sequence number for
    (year, department).

    Example:

    year = "1405"
    department = "11"

    first call -> 1
    second -> 2
    """

    row = fetch_one(
        """
        SELECT last_number
        FROM tracking_sequences
        WHERE year = ?
        AND department_code = ?
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
                ?,
                ?,
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
        SET last_number = ?
        WHERE year = ?
        AND department_code = ?
        """,
        (
            next_number,
            year,
            department_code,
        ),
    )

    return next_number
