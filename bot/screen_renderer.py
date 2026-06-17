"""Render screens and send/edit messages with optional media."""

from __future__ import annotations

import logging
from pathlib import Path

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import FSInputFile

from bot.content import PRODUCTS
from bot.navigation import Screen

logger = logging.getLogger(__name__)


async def _try_edit_text(
    bot: Bot,
    chat_id: int,
    message_id: int,
    text: str,
    reply_markup,
    parse_mode: str,
) -> bool:
    try:
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            reply_markup=reply_markup,
            parse_mode=parse_mode,
        )
        return True
    except TelegramBadRequest as exc:
        if "message is not modified" in str(exc).lower():
            return True
        logger.debug("edit_message_text failed: %s", exc)
        return False


async def _send_brochure_if_exists(
    bot: Bot,
    chat_id: int,
    pdf_path: Path | None,
    caption: str,
    parse_mode: str,
) -> None:
    if pdf_path and pdf_path.is_file():
        await bot.send_document(
            chat_id=chat_id,
            document=FSInputFile(pdf_path),
            caption=caption,
            parse_mode=parse_mode,
        )


async def show_screen(
    bot: Bot,
    *,
    chat_id: int,
    screen: Screen,
    parse_mode: str,
    menu_message_id: int | None = None,
    prefer_new_message: bool = False,
) -> int:
    """
    Display a screen by editing the menu message when possible.

    Returns the message_id of the active menu message.
    """
    keyboard = screen.keyboard_factory()
    product = PRODUCTS.get(screen.product_key) if screen.product_key else None
    image_path = product.image_path if product else None
    has_local_image = bool(image_path and image_path.is_file())

    if (
        menu_message_id
        and not prefer_new_message
        and not has_local_image
    ):
        if await _try_edit_text(
            bot, chat_id, menu_message_id, screen.text_html, keyboard, parse_mode
        ):
            return menu_message_id
        # Cannot turn a photo message into plain text — replace it.
        try:
            await bot.delete_message(chat_id=chat_id, message_id=menu_message_id)
        except TelegramBadRequest:
            pass

    if has_local_image and image_path is not None:
        if menu_message_id and not prefer_new_message:
            try:
                await bot.delete_message(chat_id=chat_id, message_id=menu_message_id)
            except TelegramBadRequest:
                pass
        sent = await bot.send_photo(
            chat_id=chat_id,
            photo=FSInputFile(image_path),
            caption=screen.text_html,
            reply_markup=keyboard,
            parse_mode=parse_mode,
        )
        if product and product.brochure_pdf_path:
            await _send_brochure_if_exists(
                bot,
                chat_id,
                product.brochure_pdf_path,
                caption="📄 Product feature brochure (PDF)",
                parse_mode=parse_mode,
            )
        return sent.message_id

    sent = await bot.send_message(
        chat_id=chat_id,
        text=screen.text_html,
        reply_markup=keyboard,
        parse_mode=parse_mode,
    )
    if product and product.brochure_pdf_path:
        await _send_brochure_if_exists(
            bot,
            chat_id,
            product.brochure_pdf_path,
            caption="📄 Product feature brochure (PDF)",
            parse_mode=parse_mode,
        )
    return sent.message_id
