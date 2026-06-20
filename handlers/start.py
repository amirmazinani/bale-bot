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

from content.loader import SCREENS
from keyboards.reply import persistent_reply_keyboard
from utils.fsm import fsm_store

logger = logging.getLogger(__name__)
router = Router(name="start")


@router.message(CommandStart())
async def on_start(message: Message) -> None:
    logger.info("user_id=%s started the bot (chat_id=%s)", message.from_user.id, message.chat.id)
    fsm_store.reset(message.chat.id)

    await message.answer(SCREENS["welcome"].text, reply_markup=persistent_reply_keyboard(), parse_mode="HTML")
    s = SCREENS["main_menu"]
    await message.answer(s.text, reply_markup=s.keyboard, parse_mode="HTML")
