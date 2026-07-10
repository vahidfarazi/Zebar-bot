"""
handlers/admin_handlers.py

Admin command handler.
"""

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
)


# -----------------------------
# Handle Admin Message
# -----------------------------
def handle_admin_message(
    chat_id: int,
    message: str,
) -> str:
    """
    Admin command handler.
    """

    if not message:

        return "پیام نامعتبر است"

    parts = message.split()

    cmd = parts[0].lower()

    # -------------------------
    # Dashboard
    # -------------------------
    if cmd == "dashboard":

        result = dashboard()

        if not result["success"]:

            return result["message"]

        stats = result["statistics"]

        return (
            "📊 داشبورد سامانه\n\n"
            f"📥 درخواست‌های باز: {stats['open']}\n"
            f"✅ درخواست‌های بسته: {stats['closed']}\n"
            f"🆕 درخواست‌های امروز: {stats['today']}\n"
            f"👨‍💼 کارشناسان فعال: {stats['experts']}"
        )

    # -------------------------
    # Statistics
    # -------------------------
    if cmd == "stats":

        result = get_statistics()

        if not result["success"]:

            return result["message"]

        stats = result["statistics"]

        return (
            f"📥 باز: {stats['open']}\n"
            f"✅ بسته: {stats['closed']}\n"
            f"🆕 امروز: {stats['today']}\n"
            f"👨‍💼 کارشناسان: {stats['experts']}"
        )

    # -------------------------
    # Recent Requests
    # -------------------------
    if cmd == "recent":

        result = get_recent_activity()

        if not result["success"]:

            return result["message"]

        rows = result["recent_requests"]

        if not rows:

            return "درخواستی وجود ندارد."

        text = "📋 آخرین درخواست‌ها\n\n"

        for row in rows:

            text += (
                f"{row['tracking_code']} | "
                f"{row['service']} | "
                f"{row['status']}\n"
            )

        return text

    # -------------------------
    # Create Expert
    # -------------------------
    if cmd == "create_expert":

        if len(parts) < 5:

            return "فرمت: create_expert chat_id name username department"

        result = create_expert_account(

            int(parts[1]),

            parts[2],

            parts[3],

            parts[4],

        )

        return "انجام شد" if result["success"] else result["message"]

    # -------------------------
    # Deactivate Expert
    # -------------------------
    if cmd == "deactivate_expert":

        if len(parts) < 2:

            return "فرمت: deactivate_expert chat_id"

        result = deactivate_expert(

            int(parts[1]),

        )

        return "انجام شد" if result["success"] else result["message"]

    # -------------------------
    # Transfer Request
    # -------------------------
    if cmd == "transfer":

        if len(parts) < 3:

            return "فرمت: transfer request_id expert_id"

        result = transfer_request(

            int(parts[1]),

            int(parts[2]),

        )

        return "انجام شد" if result["success"] else result["message"]

    # -------------------------
    # Add Holiday
    # -------------------------
    if cmd == "add_holiday":

        if len(parts) < 2:

            return "فرمت: add_holiday YYYY-MM-DD"

        result = add_system_holiday(

            parts[1],

        )

        return "انجام شد" if result["success"] else result["message"]

    # -------------------------
    # Remove Holiday
    # -------------------------
    if cmd == "remove_holiday":

        if len(parts) < 2:

            return "فرمت: remove_holiday YYYY-MM-DD"

        result = delete_system_holiday(

            parts[1],

        )

        return "انجام شد" if result["success"] else result["message"]

    # -------------------------
    # Update Settings
    # -------------------------
    if cmd == "set":

        if len(parts) < 3:

            return "فرمت: set key value"

        result = update_settings(

            parts[1],

            " ".join(parts[2:]),

        )

        return "انجام شد" if result["success"] else result["message"]

    return "دستور نامعتبر است"
