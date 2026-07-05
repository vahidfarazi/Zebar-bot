"""
bale/keyboards.py

Keyboard builders.
"""


# -----------------------------
# Reply Keyboard
# -----------------------------
def reply_keyboard(rows):

    keyboard = []

    for row in rows:

        buttons = []

        for text in row:

            buttons.append({

                "text": text,

            })

        keyboard.append(buttons)

    return {

        "keyboard": keyboard,

        "resize_keyboard": True,

    }


# -----------------------------
# Inline Keyboard
# -----------------------------
def inline_keyboard(rows):

    keyboard = []

    for row in rows:

        buttons = []

        for text, callback in row:

            buttons.append({

                "text": text,

                "callback_data": callback,

            })

        keyboard.append(buttons)

    return {

        "inline_keyboard": keyboard,

    }
