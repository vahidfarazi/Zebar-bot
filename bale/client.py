"""
bale/client.py

HTTP client for Bale Bot API.
"""

import requests

from logger import (
    log_error,
)

from .constants import (
    BASE_URL,
)


# -----------------------------
# POST
# -----------------------------
def post(
    method: str,
    payload: dict,
):

    url = BASE_URL + method

    try:

        response = requests.post(

            url,

            json=payload,

            timeout=20,

        )

        response.raise_for_status()

        data = response.json()

        if not data.get(
            "ok",
            False,
        ):

            raise Exception(str(data))

        return data

    except Exception as e:

        log_error(

            "bale",

            method,

            str(e),

        )

        return None
