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

VALIDATORS = {
    "request_number": validate_request_number,
    "national_code": validate_national_code,
    "mobile": validate_mobile,
    "computer_code": validate_computer_code,
    "bill_id": validate_bill_id,
}


class FormEngine:

    def __init__(self, form: list):

        self.form = form

    # -----------------------------
    # First Step
    # -----------------------------
    def first_step(self):

        return self.form[0]

    # -----------------------------
    # Next Step
    # -----------------------------
    def next_step(
        self,
        current_state: str,
    ):

        for index, item in enumerate(self.form):

            if item["state"] == current_state:

                if index + 1 >= len(self.form):
                    return None

                return self.form[index + 1]

        return None

    # -----------------------------
    # Current Step
    # -----------------------------
    def current_step(
        self,
        state: str,
    ):

        for item in self.form:

            if item["state"] == state:
                return item

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
            step["validator"]
        )

        if validator is None:
            return False

        return validator(value)
