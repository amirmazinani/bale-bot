"""
handlers/reply_menu.py
=======================
Handlers for the two persistent Reply Keyboard buttons:
    🏠 Main Menu
    📞 Contact / Support

These match on literal message text (that's how Telegram/Bale reply
keyboards work -- tapping a button just sends its label as a normal text
message). Because they always send a NEW message (there's nothing to edit;
a reply-keyboard tap isn't a CallbackQuery), every other inline-menu screen
opened from here starts a fresh "edit chain" that subsequent inline taps
will edit in place.
"""

from __future__ import annotations

import logging

from aiogram import F, Router
from aiogram.types import Message

from content.loader import SCREENS
from keyboards.reply import BTN_CONTACT, BTN_MAIN_MENU
from utils.fsm import fsm_store
from utils.screen import send_screen

logger = logging.getLogger(__name__)
router = Router(name="reply_menu")


@router.message(F.text == BTN_MAIN_MENU)
async def on_main_menu_button(message: Message) -> None:
    logger.info("user_id=%s opened Main Menu via reply keyboard", message.from_user.id)
    fsm_store.reset(message.chat.id)
    s = SCREENS["main_menu"]
    await send_screen(message, s.text, s.keyboard)


@router.message(F.text == BTN_CONTACT)
async def on_contact_button(message: Message) -> None:
    logger.info("user_id=%s opened Contact via reply keyboard", message.from_user.id)
    s = SCREENS["contact"]
    await send_screen(message, s.text, s.keyboard)
