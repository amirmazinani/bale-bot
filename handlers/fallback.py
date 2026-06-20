"""
handlers/fallback.py
======================
Catch-all for any text message that isn't:
  - /start
  - one of the two persistent reply-keyboard labels
  - the demo-info free-text capture (handled & consumed earlier)

Registered LAST (see bot.py router include order) so it only ever fires
when nothing more specific matched. This guarantees the user always gets a
helpful response instead of silence, fulfilling "user never gets stuck"
for the free-text case as well as the button case.
"""

from __future__ import annotations

import logging

from aiogram import F, Router
from aiogram.types import Message

from content.loader import SCREENS

logger = logging.getLogger(__name__)
router = Router(name="fallback")


@router.message(F.text)
async def on_unrecognized_text(message: Message) -> None:
    logger.info("Unrecognized free text from user_id=%s: %r", message.from_user.id, message.text)
    s = SCREENS["main_menu"]
    await message.answer("🤔 متوجه نشدم. منوی اصلی:")
    await message.answer(s.text, reply_markup=s.keyboard, parse_mode="HTML")