"""Shared handler dependencies and navigation helper."""

from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram import Bot
from aiogram.types import User

from bot import callbacks as cb
from bot.activity_logger import ActivityLogger
from bot.menu_state import MenuStateStore
from bot.navigation import Screen, get_screen
from bot.screen_renderer import show_screen

if TYPE_CHECKING:
    from bot.config import Settings


async def log_user_action(
    logger: ActivityLogger,
    user: User,
    action_type: str,
    action_payload: str,
    screen_id: str | None = None,
) -> None:
    full_name = " ".join(filter(None, [user.first_name, user.last_name]))
    await logger.log(
        user_id=user.id,
        username=user.username,
        full_name=full_name or None,
        action_type=action_type,
        action_payload=action_payload,
        screen_id=screen_id,
    )


async def navigate_to(
    bot: Bot,
    *,
    chat_id: int,
    user: User,
    route_id: str,
    settings: Settings,
    activity_logger: ActivityLogger,
    menu_state: MenuStateStore,
    action_type: str,
    action_payload: str,
    prefer_new_message: bool = False,
) -> None:
    screen = get_screen(route_id)
    if screen is None:
        screen = get_screen(cb.MAIN)
    assert screen is not None

    await log_user_action(
        activity_logger,
        user,
        action_type,
        action_payload,
        screen_id=screen.screen_id,
    )

    menu_message_id = menu_state.get_menu_message(chat_id)
    new_message_id = await show_screen(
        bot,
        chat_id=chat_id,
        screen=screen,
        parse_mode=settings.parse_mode,
        menu_message_id=menu_message_id,
        prefer_new_message=prefer_new_message,
    )
    menu_state.set_menu_message(chat_id, new_message_id)
