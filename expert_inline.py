"""
expert_inline.py

Inline buttons for expert group.
"""

def expert_request_keyboard(tracking: str):

    return [

        [

            ("💬 پاسخ", f"reply:{tracking}"),

            ("🔄 ارجاع", f"forward:{tracking}"),

        ],

    ]
