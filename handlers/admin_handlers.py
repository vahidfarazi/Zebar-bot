"""
handlers/admin_handlers.py

Admin command handler.
"""

from database import is_admin

from menus import (
    ADMIN_MENU,
    MAIN_MENU,
)

from admin_service import (
    create_expert_account,
    deactivate_expert,
    transfer_request,
    add_system_holiday,
    delete_system_holiday,
    update_settings,
    dashboard,
    get_statistics,
    get_recent_activity,
    get_daily_report,
    get_weekly_report,
    get_monthly_report,
)


def handle_admin_message(
    chat_id: int,
    message: str,
):

    if not is_admin(chat_id):
        return {
            "text": "⛔ شما دسترسی به پنل مدیریت ندارید.",
        }

    if message == "/admin":
        return {
            "text": "پنل مدیریت",
            "keyboard": ADMIN_MENU,
        }

    if message == "🏠 منوی اصلی":
        return {
            "text": "منوی اصلی",
            "keyboard": MAIN_MENU,
        }

    if not message:
        return {
            "text": "پیام نامعتبر است",
        }

    parts = message.split()
    cmd = parts[0].lower()

    # -------------------------
    # Dashboard
    # -------------------------
    if cmd == "dashboard" or message == "📊 داشبورد":

        result = dashboard()

        if not result["success"]:
            return {
                "text": result["message"],
            }

        stats = result["statistics"]

        return {
            "text": (
                "📊 داشبورد سامانه\n\n"
                f"📥 درخواست‌های باز: {stats['open']}\n"
                f"✅ درخواست‌های بسته: {stats['closed']}\n"
                f"🆕 درخواست‌های امروز: {stats['today']}\n"
                f"👨‍💼 کارشناسان فعال: {stats['experts']}"
            ),
            "keyboard": ADMIN_MENU,
        }

    # -------------------------
    # Statistics
    # -------------------------
    if cmd == "stats" or message == "📈 آمار":

        result = get_statistics()

        if not result["success"]:
            return {
                "text": result["message"],
                "keyboard": ADMIN_MENU,
            }

        stats = result["statistics"]

        return {
            "text": (
                f"📥 باز: {stats['open']}\n"
                f"✅ بسته: {stats['closed']}\n"
                f"🆕 امروز: {stats['today']}\n"
                f"👨‍💼 کارشناسان: {stats['experts']}"
            ),
            "keyboard": ADMIN_MENU,
        }

    # -------------------------
    # Daily Report
    # -------------------------
    if cmd == "daily" or message == "📅 گزارش روزانه":

        result = get_daily_report()

        if not result["success"]:
            return {
                "text": result["message"],
                "keyboard": ADMIN_MENU,
            }

        report = result["report"]

        return {
            "text": (
                "📅 گزارش روزانه\n\n"
                f"📥 کل درخواست‌ها: {report['total']}\n"
                f"🟢 باز: {report['open']}\n"
                f"✅ بسته: {report['closed']}"
            ),
            "keyboard": ADMIN_MENU,
        }

    # -------------------------
    # Weekly Report
    # -------------------------
    if cmd == "weekly" or message == "📆 گزارش هفتگی":

        result = get_weekly_report()

        if not result["success"]:
            return {
                "text": result["message"],
                "keyboard": ADMIN_MENU,
            }

        report = result["report"]

        return {
            "text": (
                "📆 گزارش هفتگی\n\n"
                f"📥 کل درخواست‌ها: {report['total']}\n"
                f"🟢 باز: {report['open']}\n"
                f"✅ بسته: {report['closed']}"
            ),
            "keyboard": ADMIN_MENU,
        }

    # -------------------------
    # Monthly Report
    # -------------------------
    if cmd == "monthly" or message == "🗓 گزارش ماهانه":

        result = get_monthly_report()

        if not result["success"]:
            return {
                "text": result["message"],
                "keyboard": ADMIN_MENU,
            }

        report = result["report"]

        return {
            "text": (
                "🗓 گزارش ماهانه\n\n"
                f"📥 کل درخواست‌ها: {report['total']}\n"
                f"🟢 باز: {report['open']}\n"
                f"✅ بسته: {report['closed']}"
            ),
            "keyboard": ADMIN_MENU,
        }

    # -------------------------
    # Recent Requests
    # -------------------------
    if cmd == "recent" or message == "📋 درخواست‌های اخیر":

        result = get_recent_activity()

        if not result["success"]:
            return {
                "text": result["message"],
                "keyboard": ADMIN_MENU,
            }

        rows = result["recent_requests"]

        if not rows:
            return {
                "text": "درخواستی وجود ندارد.",
                "keyboard": ADMIN_MENU,
            }

        text = "📋 آخرین درخواست‌ها\n\n"

        for row in rows:
            text += (
                f"{row['tracking_code']} | "
                f"{row['service']} | "
                f"{row['status']}\n"
            )

        return {
            "text": text,
            "keyboard": ADMIN_MENU,
        }

    # -------------------------
    # Create Expert
    # -------------------------
    if cmd == "create_expert":

        if len(parts) < 5:
            return {
                "text": "فرمت: create_expert chat_id name username department",
                "keyboard": ADMIN_MENU,
            }

        result = create_expert_account(
            int(parts[1]),
            parts[2],
            parts[3],
            parts[4],
        )

        return {
            "text": "انجام شد" if result["success"] else result["message"],
            "keyboard": ADMIN_MENU,
        }

    # -------------------------
    # Deactivate Expert
    # -------------------------
    if cmd == "deactivate_expert":

        if len(parts) < 2:
            return {
                "text": "فرمت: deactivate_expert chat_id",
                "keyboard": ADMIN_MENU,
            }

        result = deactivate_expert(
            int(parts[1]),
        )

        return {
            "text": "انجام شد" if result["success"] else result["message"],
            "keyboard": ADMIN_MENU,
        }

    # -------------------------
    # Transfer Request
    # -------------------------
    if cmd == "transfer":

        if len(parts) < 3:
            return {
                "text": "فرمت: transfer request_id expert_id",
                "keyboard": ADMIN_MENU,
            }

        result = transfer_request(
            int(parts[1]),
            int(parts[2]),
        )

        return {
            "text": "انجام شد" if result["success"] else result["message"],
            "keyboard": ADMIN_MENU,
        }

    # -------------------------
    # Add Holiday
    # -------------------------
    if cmd == "add_holiday":

        if len(parts) < 2:
            return {
                "text": "فرمت: add_holiday YYYY-MM-DD",
                "keyboard": ADMIN_MENU,
            }

        result = add_system_holiday(parts[1])

        return {
            "text": "انجام شد" if result["success"] else result["message"],
            "keyboard": ADMIN_MENU,
        }

    # -------------------------
    # Remove Holiday
    # -------------------------
    if cmd == "remove_holiday":

        if len(parts) < 2:
            return {
                "text": "فرمت: remove_holiday YYYY-MM-DD",
                "keyboard": ADMIN_MENU,
            }

        result = delete_system_holiday(parts[1])

        return {
            "text": "انجام شد" if result["success"] else result["message"],
            "keyboard": ADMIN_MENU,
        }

    # -------------------------
    # Update Settings
    # -------------------------
    if cmd == "set":

        if len(parts) < 3:
            return {
                "text": "فرمت: set key value",
                "keyboard": ADMIN_MENU,
            }

        result = update_settings(
            parts[1],
            " ".join(parts[2:]),
        )

        return {
            "text": "انجام شد" if result["success"] else result["message"],
            "keyboard": ADMIN_MENU,
        }

    return {
        "text": "دستور نامعتبر است.",
        "keyboard": ADMIN_MENU,
            }
