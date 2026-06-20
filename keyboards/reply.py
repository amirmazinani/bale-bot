"""
keyboards/reply.py
===================
The persistent bottom Reply Keyboard. Per the requirements, this is ALWAYS
visible and contains exactly two buttons:

    🏠 Main Menu          -- jumps straight back to the main menu at any time
    📞 Contact / Support  -- jumps straight to contact info at any time

Reply keyboard buttons send their label back as a normal text Message
(not a callback), so handlers/reply_menu.py matches on the literal text.
This is intentional UX: the bottom bar is for "escape hatches" the user can
hit even if they're lost or an inline keyboard failed to render, while all
*nested* navigation uses inline keyboards (kept clean, edited in place).
"""

from __future__ import annotations

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

BTN_MAIN_MENU = "🏠 منو اصلی"
BTN_CONTACT = "📞 تماس / پشتیبانی"


def persistent_reply_keyboard() -> ReplyKeyboardMarkup:
    """The always-visible bottom keyboard, sent once and left in place."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_MAIN_MENU), KeyboardButton(text=BTN_CONTACT)],
        ],
        resize_keyboard=True,
        is_persistent=True,   # keeps it visible even after other prompts
        input_field_placeholder="پیامی بنویس یا از منوی زیر استفاده کن…",
    )
