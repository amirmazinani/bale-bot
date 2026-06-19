"""
handlers/start.py
==================
The /start command: greets the user, attaches the persistent reply
keyboard (sent exactly once here -- it then stays visible for the whole
conversation per Telegram/Bale client behavior), and shows the main menu.
"""

from __future__ import annotations

import logging

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from content.erp_content import MAIN_MENU_PROMPT_HTML, WELCOME_HTML
from keyboards.inline import main_menu_keyboard
from keyboards.reply import persistent_reply_keyboard
from utils.fsm import fsm_store

logger = logging.getLogger(__name__)
router = Router(name="start")


@router.message(CommandStart())
async def on_start(message: Message) -> None:
    logger.info("user_id=%s started the bot (chat_id=%s)", message.from_user.id, message.chat.id)
    fsm_store.reset(message.chat.id)

    # Step 1: attach the persistent bottom reply keyboard.
    await message.answer(WELCOME_HTML, reply_markup=persistent_reply_keyboard(), parse_mode="HTML")

    # Step 2: show the main inline menu as its own message, which all
    # subsequent inline taps will edit in place.
    await message.answer(MAIN_MENU_PROMPT_HTML, reply_markup=main_menu_keyboard(), parse_mode="HTML")
