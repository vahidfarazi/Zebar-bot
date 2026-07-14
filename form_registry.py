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



# =================================================
# Forms Registry
# =================================================

FORMS = {

    "NEW_CONNECTION":
        NEW_CONNECTION_FORM,

    "AFTER_SALES":
        AFTER_SALES_FORM,

    "METER_TEST":
        METER_TEST_FORM,

    "BILL_INQUIRY":
        BILL_INQUIRY_FORM,

}



# =================================================
# Get Form
# =================================================

def get_form(
    service: str,
) -> list:


    if not service:

        return []


    return FORMS.get(

        service,

        [],

    )



# =================================================
# Check Form Exists
# =================================================

def has_form(
    service: str,
) -> bool:


    return (

        service in FORMS

        and bool(
            FORMS[service]
        )

    )



# =================================================
# List Forms
# =================================================

def list_forms() -> list[str]:


    return list(
        FORMS.keys()
    )
