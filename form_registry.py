"""
form_registry.py

Central registry for request forms.
"""

from forms import (
    NEW_CONNECTION_FORM,
    AFTER_SALES_FORM,
    METER_TEST_FORM,
    BILL_INQUIRY_FORM,
)


# -----------------------------
# Forms
# -----------------------------
FORMS = {

    "NEW_CONNECTION": NEW_CONNECTION_FORM,

    "AFTER_SALES": AFTER_SALES_FORM,

    "METER_TEST": METER_TEST_FORM,

    "BILL_INQUIRY": BILL_INQUIRY_FORM,

}


# -----------------------------
# Get Form
# -----------------------------
def get_form(
    service: str,
) -> list:

    return FORMS.get(
        service,
        [],
    )
