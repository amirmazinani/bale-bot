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

from content.loader import REPLY_KEYBOARD_BUTTONS

# Get button texts for handlers
REPLY_BUTTON_TEXTS: list[str] = [b["text"] for b in REPLY_KEYBOARD_BUTTONS]


def persistent_reply_keyboard() -> ReplyKeyboardMarkup:
    # Create a single row with all buttons
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=b["text"]) for b in REPLY_KEYBOARD_BUTTONS]],
        resize_keyboard=True,
        is_persistent=True,
        input_field_placeholder="پیام بنویسید یا از منو استفاده کنید…",
    )
