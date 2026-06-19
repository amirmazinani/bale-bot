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

from config import settings
from content.erp_content import MAIN_MENU_PROMPT_HTML, contact_html
from keyboards.inline import contact_keyboard, main_menu_keyboard
from keyboards.reply import BTN_CONTACT, BTN_MAIN_MENU
from utils.fsm import fsm_store
from utils.screen import send_screen

logger = logging.getLogger(__name__)
router = Router(name="reply_menu")


@router.message(F.text == BTN_MAIN_MENU)
async def on_main_menu_button(message: Message) -> None:
    logger.info("user_id=%s opened Main Menu via reply keyboard", message.from_user.id)
    # Pressing Main Menu always cancels any pending text-capture flow
    # (e.g. an unfinished demo-request) so the user can't get "stuck" mid-flow.
    fsm_store.reset(message.chat.id)
    await send_screen(message, MAIN_MENU_PROMPT_HTML, main_menu_keyboard())


@router.message(F.text == BTN_CONTACT)
async def on_contact_button(message: Message) -> None:
    logger.info("user_id=%s opened Contact via reply keyboard", message.from_user.id)
    text = contact_html(
        settings.COMPANY_NAME,
        settings.SUPPORT_PHONE,
        settings.SUPPORT_EMAIL,
        settings.SALES_BALE_USERNAME,
        settings.COMPANY_WEBSITE,
    )
    await send_screen(message, text, contact_keyboard())
