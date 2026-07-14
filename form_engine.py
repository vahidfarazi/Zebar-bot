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
    validate_subscription,
    validate_meter_serial,
    detect_identifier,
)



# =================================================
# Validators
# =================================================

VALIDATORS = {

    "request_number":
        validate_request_number,

    "national_code":
        validate_national_code,

    "mobile":
        validate_mobile,

    "computer_code":
        validate_computer_code,

    "bill_id":
        validate_bill_id,

    "subscription":
        validate_subscription,

    "meter_serial":
        validate_meter_serial,

}



# =================================================
# Form Engine
# =================================================

class FormEngine:


    def __init__(
        self,
        form:list,
    ):

        self.form = form or []



    # ---------------------------------------------
    # First Step
    # ---------------------------------------------

    def first_step(
        self,
    ) -> dict | None:


        if not self.form:

            return None


        return self.form[0]



    # ---------------------------------------------
    # Current Step
    # ---------------------------------------------

    def current_step(
        self,
        state:str,
    ) -> dict | None:


        for step in self.form:

            if step.get("state") == state:

                return step


        return None



    # ---------------------------------------------
    # Next Step
    # ---------------------------------------------

    def next_step(
        self,
        state:str,
    ) -> dict | None:


        for index, step in enumerate(self.form):

            if step.get("state") == state:


                if index + 1 >= len(self.form):

                    return None


                return self.form[index + 1]


        return None



    # ---------------------------------------------
    # Previous Step
    # ---------------------------------------------

    def previous_step(
        self,
        state:str,
    ) -> dict | None:


        for index, step in enumerate(self.form):

            if step.get("state") == state:


                if index == 0:

                    return None


                return self.form[index - 1]


        return None



    # ---------------------------------------------
    # Validate
    # ---------------------------------------------

    def validate(
        self,
        state:str,
        value:str,
    ) -> bool:


        step = self.current_step(
            state,
        )


        if step is None:

            return False



        validator = step.get(
            "validator",
        )



        if validator == "ONE_OF":

            return (
                detect_identifier(value)
                is not None
            )



        func = VALIDATORS.get(
            validator,
        )


        if func is None:

            return False



        return func(
            value,
        )



    # ---------------------------------------------
    # Detect Field
    # ---------------------------------------------

    def detect_field(
        self,
        state:str,
        value:str,
    ) -> str | None:


        step = self.current_step(
            state,
        )


        if step is None:

            return None



        if step.get("validator") == "ONE_OF":

            return detect_identifier(
                value,
            )


        return step.get(
            "field",
        )



    # ---------------------------------------------
    # Field Name
    # ---------------------------------------------

    def field_name(
        self,
        state:str,
    ) -> str | None:


        step = self.current_step(
            state,
        )


        if step is None:

            return None


        return step.get(
            "field",
        )



    # ---------------------------------------------
    # Title
    # ---------------------------------------------

    def title(
        self,
        state:str,
    ) -> str:


        step = self.current_step(
            state,
        )


        if step is None:

            return ""


        return step.get(
            "title",
            "",
        )



    # ---------------------------------------------
    # Last Step
    # ---------------------------------------------

    def is_last_step(
        self,
        state:str,
    ) -> bool:


        return (
            self.next_step(state)
            is None
        )



    # ---------------------------------------------
    # Count
    # ---------------------------------------------

    def step_count(
        self,
    ) -> int:


        return len(
            self.form,
        )



    # ---------------------------------------------
    # States
    # ---------------------------------------------

    def states(
        self,
    ) -> list:


        return [

            step.get(
                "state"
            )

            for step in self.form

        ]
