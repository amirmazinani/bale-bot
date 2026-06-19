"""
utils/screen.py
================
Implements the "edit the message in place" UX for inline navigation.

Per the requirement "Clicking [Our Products] EDITS the message" rather than
sending a new one (which would clutter the chat), every inline-menu
transition should go through `render_screen()` below when triggered from a
CallbackQuery, and through `send_screen()` when it's the very first message
of a flow (e.g. /start, or a reply-keyboard button press, which cannot edit
a previous message because there may not be one in the same context).

Both helpers share the same signature shape so handlers don't need to
think about which one to use beyond "callback -> render_screen,
fresh message -> send_screen".
"""

from __future__ import annotations

import logging

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message

logger = logging.getLogger(__name__)

PARSE_MODE = "HTML"


async def render_screen(
    callback: CallbackQuery,
    text: str,
    keyboard: InlineKeyboardMarkup,
) -> None:
    """
    Edit the message behind a CallbackQuery to show a new screen.

    Falls back to sending a new message if editing fails (e.g. the original
    message was a photo/document and can't be turned into plain text, or it
    was deleted) -- this guarantees the user is never stuck looking at a
    stale screen with no working buttons.
    """
    if callback.message is None:
        logger.warning("CallbackQuery without a message; cannot render screen.")
        return

    try:
        await callback.message.edit_text(text, reply_markup=keyboard, parse_mode=PARSE_MODE)
    except TelegramBadRequest as exc:
        # Common benign case: "message is not modified" when the user
        # double-taps the same button. Anything else, log and recover by
        # sending a fresh message so navigation never silently breaks.
        if "message is not modified" in str(exc).lower():
            logger.debug("Ignoring no-op edit (message not modified).")
        else:
            logger.warning("edit_text failed (%s); sending a new message instead.", exc)
            await callback.message.answer(text, reply_markup=keyboard, parse_mode=PARSE_MODE)


async def send_screen(
    message: Message,
    text: str,
    keyboard: InlineKeyboardMarkup,
) -> None:
    """Send a brand-new message containing an inline-keyboard screen."""
    await message.answer(text, reply_markup=keyboard, parse_mode=PARSE_MODE)


async def safe_answer_callback(callback: CallbackQuery, text: str | None = None) -> None:
    """
    Always acknowledge the callback query (stops the client-side loading
    spinner on the tapped button), swallowing the harmless "query too old /
    invalid" error that happens if the user taps a button from a very old
    message after the callback has expired.
    """
    try:
        await callback.answer(text)
    except TelegramBadRequest as exc:
        logger.debug("callback.answer() failed harmlessly: %s", exc)
