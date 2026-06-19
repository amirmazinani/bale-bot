"""
bot_instance.py
================
Builds the aiogram Bot instance pointed at Bale's API instead of Telegram's.

How the Bale override works
----------------------------
aiogram's AiohttpSession builds request URLs via two format-string
templates:
    api: "https://api.telegram.org/bot{token}/{method}"
    file: "https://api.telegram.org/file/bot{token}/{path}"

By constructing the Session with `api=TelegramAPIServer(base, file)` we
swap those templates for Bale's equivalents (from config.settings), while
every other piece of aiogram -- update parsing, keyboard objects, FSM,
filters -- is completely unaware that it isn't talking to Telegram. This is
exactly the "shared architecture" trick the requirements describe, and it's
the ONLY place in the whole codebase that needs to know about that fact.

To point this same code at real Telegram for local testing, just set the
BOT_API_BASE_URL_TEMPLATE / BOT_API_FILE_URL_TEMPLATE env vars to Telegram's
defaults (see config.py docstring).
"""

from __future__ import annotations

from aiogram import Bot
from aiogram.client.bot import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from aiogram.enums import ParseMode

from config import settings


def build_bot() -> Bot:
    """Construct an aiogram Bot wired to Bale's API endpoint."""
    bale_server = TelegramAPIServer(
        base=settings.API_BASE_URL_TEMPLATE,
        file=settings.API_FILE_URL_TEMPLATE,
    )
    session = AiohttpSession(api=bale_server)

    bot = Bot(
        token=settings.BOT_TOKEN,
        session=session,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    return bot
