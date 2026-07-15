"""
database/tracking_sequence.py

Tracking sequence repository.
"""

from .crud import (
    execute,
    fetch_one,
)


# =================================================
# Get Next Tracking Number
# =================================================

def get_next_tracking_number(
    year: str,
    department_code: str,
) -> int:
    """
    Return next sequence number.
    """

    row = fetch_one(
        """
        SELECT last_number

        FROM tracking_sequences

        WHERE year=%s

        AND department_code=%s
        """,
        (
            year,
            department_code,
        ),
    )


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

            ON CONFLICT(year, department_code)

            DO NOTHING
            """,
            (
                year,
                department_code,
            ),
        )

        return 1



    next_number = (
        row["last_number"] + 1
    )


    execute(
        """
        UPDATE tracking_sequences

        SET last_number=%s

        WHERE year=%s

        AND department_code=%s
        """,
        (
            next_number,
            year,
            department_code,
        ),
    )


    return next_number



# =================================================
# Get Current Sequence
# =================================================

def get_current_sequence(
    year: str,
    department_code: str,
) -> int:

    row = fetch_one(
        """
        SELECT last_number

        FROM tracking_sequences

        WHERE year=%s

        AND department_code=%s
        """,
        (
            year,
            department_code,
        ),
    )

    if not row:

        return 0

    return row["last_number"] or 0



# =================================================
# Format Tracking Code
# =================================================

def format_tracking_number(
    year: str,
    department_code: str,
    number: int,
) -> str:
    """
    Generate tracking code.

    Example:
        SR-2026-IT-000001
    """

    return (
        f"SR-{year}-"
        f"{department_code}-"
        f"{number:06d}"
    )



# =================================================
# Reset Sequence
# =================================================

def reset_sequence(
    year: str,
    department_code: str,
) -> None:

    execute(
        """
        UPDATE tracking_sequences

        SET last_number=0

        WHERE year=%s

        AND department_code=%s
        """,
        (
            year,
            department_code,
        ),
    )
