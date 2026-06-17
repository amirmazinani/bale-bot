"""Inline keyboard callback handlers."""

from __future__ import annotations

from aiogram import F, Router
from aiogram.types import CallbackQuery

from bot.activity_logger import ActivityLogger
from bot.config import Settings
from bot.handlers.common import navigate_to
from bot.menu_state import MenuStateStore
from bot.navigation import ROUTES, get_screen

router = Router(name="callbacks")

# All known inline route tokens (including dynamic demo:* resolved via get_screen).
KNOWN_CALLBACKS = set(ROUTES.keys())


@router.callback_query(F.data.in_(KNOWN_CALLBACKS))
async def on_inline_navigation(
    callback: CallbackQuery,
    settings: Settings,
    activity_logger: ActivityLogger,
    menu_state: MenuStateStore,
) -> None:
    if callback.data is None or callback.from_user is None or callback.message is None:
        await callback.answer()
        return

    chat_id = callback.message.chat.id
    menu_state.set_menu_message(chat_id, callback.message.message_id)

    await navigate_to(
        callback.bot,
        chat_id=chat_id,
        user=callback.from_user,
        route_id=callback.data,
        settings=settings,
        activity_logger=activity_logger,
        menu_state=menu_state,
        action_type="inline_callback",
        action_payload=callback.data,
    )
    await callback.answer()


@router.callback_query(F.data.startswith("demo:"))
async def on_product_demo(
    callback: CallbackQuery,
    settings: Settings,
    activity_logger: ActivityLogger,
    menu_state: MenuStateStore,
) -> None:
    if callback.data is None or callback.from_user is None or callback.message is None:
        await callback.answer()
        return

    if get_screen(callback.data) is None:
        await callback.answer("Unknown product.", show_alert=True)
        return

    chat_id = callback.message.chat.id
    menu_state.set_menu_message(chat_id, callback.message.message_id)

    await navigate_to(
        callback.bot,
        chat_id=chat_id,
        user=callback.from_user,
        route_id=callback.data,
        settings=settings,
        activity_logger=activity_logger,
        menu_state=menu_state,
        action_type="inline_callback",
        action_payload=callback.data,
    )
    await callback.answer("Demo request noted — our team will reach out soon!")
