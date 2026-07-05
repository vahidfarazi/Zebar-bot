"""
bale/parser.py

Parse Bale updates.
"""


# -----------------------------
# Message
# -----------------------------
def get_message(update: dict):

    return update.get(
        "message",
        {},
    )


# -----------------------------
# Callback
# -----------------------------
def get_callback(update: dict):

    return update.get(
        "callback_query",
        {},
    )


# -----------------------------
# Chat ID
# -----------------------------
def get_chat_id(update: dict):

    callback = get_callback(update)

    if callback:

        return callback.get(
            "message",
            {},
        ).get(
            "chat",
            {},
        ).get(
            "id",
        )

    message = get_message(update)

    return message.get(
        "chat",
        {},
    ).get(
        "id",
    )


# -----------------------------
# User ID
# -----------------------------
def get_user_id(update: dict):

    callback = get_callback(update)

    if callback:

        return callback.get(
            "from",
            {},
        ).get(
            "id",
        )

    message = get_message(update)

    return message.get(
        "from",
        {},
    ).get(
        "id",
    )


# -----------------------------
# Text
# -----------------------------
def get_text(update: dict):

    callback = get_callback(update)

    if callback:

        return callback.get(
            "data",
            "",
        )

    message = get_message(update)

    return message.get(
        "text",
        "",
    )


# -----------------------------
# Username
# -----------------------------
def get_username(update: dict):

    callback = get_callback(update)

    if callback:

        return callback.get(
            "from",
            {},
        ).get(
            "username",
            "",
        )

    message = get_message(update)

    return message.get(
        "from",
        {},
    ).get(
        "username",
        "",
    )


# -----------------------------
# Full Name
# -----------------------------
def get_full_name(update: dict):

    callback = get_callback(update)

    if callback:

        user = callback.get(
            "from",
            {},
        )

    else:

        user = get_message(update).get(
            "from",
            {},
        )

    first = user.get(
        "first_name",
        "",
    )

    last = user.get(
        "last_name",
        "",
    )

    return (first + " " + last).strip()


# -----------------------------
# Message ID
# -----------------------------
def get_message_id(update: dict):

    callback = get_callback(update)

    if callback:

        return callback.get(
            "message",
            {},
        ).get(
            "message_id",
        )

    return get_message(update).get(
        "message_id",
    )


# -----------------------------
# Is Callback
# -----------------------------
def is_callback(update: dict):

    return "callback_query" in update


# -----------------------------
# Is Message
# -----------------------------
def is_message(update: dict):

    return "message" in update
