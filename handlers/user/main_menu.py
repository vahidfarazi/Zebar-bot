"""
handlers/user/main_menu.py

Main menu handler.
"""

from menus import MAIN_MENU

from user_state import reset


# -----------------------------
# Main Menu
# -----------------------------
def handle_main_menu(
    chat_id: int,
):
    """
    Show main menu.
    """

    # خروج از هر فرم نیمه‌کاره
    reset(chat_id)

    return {
        "text": (
            "به سامانه خدمات مشترکین "
            "شرکت توزیع نیروی برق استان خراسان رضوی "
            "(آذرخش) خوش آمدید.\n\n"
            "لطفاً یکی از گزینه‌های زیر را انتخاب کنید."
        ),
        "keyboard": MAIN_MENU,
    }
