"""
form_engine.py

Generic form engine for Azarakhsh.
"""

from validators import (
    validate_request_number,
    validate_national_code,
    validate_mobile,
    validate_computer_code,
    validate_bill_id,
)


# -----------------------------
# Validators
# -----------------------------
VALIDATORS = {
    "request_number": validate_request_number,
    "national_code": validate_national_code,
    "mobile": validate_mobile,
    "computer_code": validate_computer_code,
    "bill_id": validate_bill_id,
}


class FormEngine:
    """
    Generic form processor.
    """

    def __init__(self, form: list):

        self.form = form

    # -----------------------------
    # First Step
    # -----------------------------
    def first_step(self) -> dict:

        return self.form[0]

    # -----------------------------
    # Find Step
    # -----------------------------
    def current_step(
        self,
        state: str,
    ) -> dict | None:

        for step in self.form:

            if step["state"] == state:
                return step

        return None

    # -----------------------------
    # Next Step
    # -----------------------------
    def next_step(
        self,
        state: str,
    ) -> dict | None:

        for index, step in enumerate(self.form):

            if step["state"] == state:

                if index == len(self.form) - 1:
                    return None

                return self.form[index + 1]

        return None

    # -----------------------------
    # Previous Step
    # -----------------------------
    def previous_step(
        self,
        state: str,
    ) -> dict | None:

        for index, step in enumerate(self.form):

            if step["state"] == state:

                if index == 0:
                    return None

                return self.form[index - 1]

        return None

    # -----------------------------
    # Validate
    # -----------------------------
    def validate(
        self,
        state: str,
        value: str,
    ) -> bool:

        step = self.current_step(state)

        if step is None:
            return False

        validator = VALIDATORS.get(
            step["validator"],
        )

        if validator is None:
            return False

        return validator(value)

    # -----------------------------
    # Field Name
    # -----------------------------
    def field_name(
        self,
        state: str,
    ) -> str | None:

        step = self.current_step(state)

        if step is None:
            return None

        return step["field"]

    # -----------------------------
    # Step Title
    # -----------------------------
    def title(
        self,
        state: str,
    ) -> str:

        step = self.current_step(state)

        if step is None:
            return ""

        return step["title"]

    # -----------------------------
    # Is Last Step
    # -----------------------------
    def is_last_step(
        self,
        state: str,
    ) -> bool:

        return self.next_step(state) is None

    # -----------------------------
    # Step Count
    # -----------------------------
    def step_count(self) -> int:

        return len(self.form)
