"""
keyboards.py

All keyboards for Azarakhsh Project.

Rule:
- No keyboard is allowed outside this file.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


# ---------------- BASIC KEYBOARD MODELS ---------------- #

@dataclass(frozen=True)
class Keyboard:
    """
    Simple keyboard structure.
    """
    buttons: List[List[str]]


# ---------------- MAIN MENU ---------------- #

def get_main_menu() -> Keyboard:
    return Keyboard(
        buttons=[
            ["📝 ثبت درخواست", "📋 پیگیری درخواست"],
            ["💬 ارتباط با کارشناس", "📚 راهنما"],
            ["ℹ درباره سامانه"],
        ]
    )


# ---------------- SERVICE MENU ---------------- #

def get_service_menu() -> Keyboard:
    return Keyboard(
        buttons=[
            ["⚡ برق", "💧 آب"],
            ["🏢 مشترکین", "💰 مالی"],
            ["🖥 فناوری اطلاعات"],
            ["⬅ بازگشت", "❌ لغو"],
        ]
    )


# ---------------- SUB SERVICE ---------------- #

def get_sub_service_menu() -> Keyboard:
    return Keyboard(
        buttons=[
            ["قطع برق", "افت ولتاژ"],
            ["خسارت", "جابجایی کنتور"],
            ["سایر"],
            ["⬅ بازگشت", "❌ لغو"],
        ]
    )


# ---------------- REQUEST CREATED ---------------- #

def get_request_created_menu() -> Keyboard:
    return Keyboard(
        buttons=[
            ["📋 مشاهده وضعیت", "💬 گفتگو"],
            ["🏠 منوی اصلی"],
        ]
    )


# ---------------- CHAT ---------------- #

def get_chat_menu() -> Keyboard:
    return Keyboard(
        buttons=[
            ["📎 ارسال فایل", "✅ پایان گفتگو"],
            ["🏠 منوی اصلی"],
        ]
    )


# ---------------- TRACKING ---------------- #

def get_tracking_menu() -> Keyboard:
    return Keyboard(
        buttons=[
            ["🔎 جستجو"],
            ["🏠 منوی اصلی"],
        ]
    )


# ---------------- HELP ---------------- #

def get_help_menu() -> Keyboard:
    return Keyboard(
        buttons=[
            ["📞 تماس", "🌐 سایت"],
            ["🏠 منوی اصلی"],
        ]
    )


# ---------------- ADMIN ---------------- #

def get_admin_menu() -> Keyboard:
    return Keyboard(
        buttons=[
            ["📨 درخواست‌ها", "👥 کاربران"],
            ["👨‍💼 کارشناسان", "⚙ تنظیمات"],
            ["📅 تعطیلات", "📊 آمار"],
            ["📜 لاگ سیستم", "🛠 ابزارها"],
        ]
    )


# ---------------- EXPERT ---------------- #

def get_expert_menu() -> Keyboard:
    return Keyboard(
        buttons=[
            ["📨 درخواست‌های من", "💬 گفتگوهای فعال"],
            ["📊 وضعیت", "🚪 خروج"],
        ]
    )


# ---------------- CONFIRM ---------------- #

def get_confirm_keyboard() -> Keyboard:
    return Keyboard(
        buttons=[
            ["بله", "خیر"],
        ]
    )


# ---------------- CANCEL ---------------- #

def get_cancel_keyboard() -> Keyboard:
    return Keyboard(
        buttons=[
            ["❌ لغو"],
        ]
    )


# ---------------- BACK ---------------- #

def get_back_keyboard() -> Keyboard:
    return Keyboard(
        buttons=[
            ["⬅ بازگشت"],
        ]
    )


# ---------------- HOME ---------------- #

def get_home_keyboard() -> Keyboard:
    return Keyboard(
        buttons=[
            ["🏠 منوی اصلی"],
        ]
    )


# ---------------- REMOVE KEYBOARD ---------------- #

def get_remove_keyboard():
    return None


# ---------------- INLINE KEYBOARDS ---------------- #

def get_request_inline_keyboard() -> dict:
    return {
        "inline_keyboard": [
            [
                {"text": "مشاهده جزئیات", "callback_data": "req_detail"},
                {"text": "ارجاع", "callback_data": "req_assign"},
                {"text": "بستن", "callback_data": "req_close"},
            ]
        ]
    }


def get_tracking_inline_keyboard() -> dict:
    return {
        "inline_keyboard": [
            [
                {"text": "نمایش وضعیت", "callback_data": "track_status"}
            ]
        ]
    }


def get_chat_inline_keyboard() -> dict:
    return {
        "inline_keyboard": [
            [
                {"text": "پاسخ", "callback_data": "chat_reply"},
                {"text": "ارسال فایل", "callback_data": "chat_file"},
            ]
        ]
    }
