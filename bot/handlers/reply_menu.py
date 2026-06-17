"""Reply-keyboard (bottom menu) handlers."""

from __future__ import annotations

from aiogram import F, Router
from aiogram.types import Message

from bot import callbacks as cb
from bot.activity_logger import ActivityLogger
from bot.config import Settings
from bot.handlers.common import navigate_to
from bot.keyboards import persistent_reply_keyboard
from bot.menu_state import MenuStateStore

router = Router(name="reply_menu")


@router.message(F.text == cb.REPLY_MAIN_MENU)
async def reply_main_menu(
    message: Message,
    settings: Settings,
    activity_logger: ActivityLogger,
    menu_state: MenuStateStore,
) -> None:
    user = message.from_user
    if user is None or message.chat is None:
        return

    await navigate_to(
        message.bot,
        chat_id=message.chat.id,
        user=user,
        route_id=cb.MAIN,
        settings=settings,
        activity_logger=activity_logger,
        menu_state=menu_state,
        action_type="reply_keyboard",
        action_payload=cb.REPLY_MAIN_MENU,
    )


@router.message(F.text == cb.REPLY_CONTACT)
async def reply_contact(
    message: Message,
    settings: Settings,
    activity_logger: ActivityLogger,
    menu_state: MenuStateStore,
) -> None:
    user = message.from_user
    if user is None or message.chat is None:
        return

    await navigate_to(
        message.bot,
        chat_id=message.chat.id,
        user=user,
        route_id=cb.CONTACT,
        settings=settings,
        activity_logger=activity_logger,
        menu_state=menu_state,
        action_type="reply_keyboard",
        action_payload=cb.REPLY_CONTACT,
    )


@router.message(F.text)
async def free_text_logger(
    message: Message,
    activity_logger: ActivityLogger,
) -> None:
    """Log free-form user messages (e.g. demo request details) without breaking flow."""
    user = message.from_user
    if user is None or not message.text:
        return

    from bot.handlers.common import log_user_action

    await log_user_action(
        activity_logger,
        user,
        action_type="free_text",
        action_payload=message.text,
    )

    await message.answer(
        "Thanks! Your message was recorded. "
        "Use <b>🏠 Main Menu</b> below to continue browsing, "
        "or wait for our team to follow up.",
        parse_mode="HTML",
        reply_markup=persistent_reply_keyboard(),
    )
