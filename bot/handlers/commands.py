"""Command handlers (/start, /help)."""

from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from bot import callbacks as cb
from bot.activity_logger import ActivityLogger
from bot.config import Settings
from bot.handlers.common import log_user_action, navigate_to
from bot.keyboards import persistent_reply_keyboard
from bot.menu_state import MenuStateStore

router = Router(name="commands")


@router.message(CommandStart())
async def cmd_start(
    message: Message,
    settings: Settings,
    activity_logger: ActivityLogger,
    menu_state: MenuStateStore,
) -> None:
    user = message.from_user
    if user is None or message.chat is None:
        return

    await log_user_action(activity_logger, user, "command", "/start", screen_id="welcome")

    await message.answer(
        "Keyboard loaded. Use the buttons below or the inline menu.",
        reply_markup=persistent_reply_keyboard(),
    )

    await navigate_to(
        message.bot,
        chat_id=message.chat.id,
        user=user,
        route_id="welcome",
        settings=settings,
        activity_logger=activity_logger,
        menu_state=menu_state,
        action_type="navigation",
        action_payload="welcome",
        prefer_new_message=True,
    )


@router.message(Command("help"))
async def cmd_help(
    message: Message,
    activity_logger: ActivityLogger,
) -> None:
    user = message.from_user
    if user is None:
        return

    await log_user_action(activity_logger, user, "command", "/help")

    await message.answer(
        "<b>Quick help</b>\n\n"
        "• <b>🏠 Main Menu</b> — return to the main inline menu\n"
        "• <b>📞 Contact / Support</b> — sales & support details\n"
        "• Use inline buttons to browse products and pricing\n"
        "• Every screen includes <b>🔙 Back</b> so you never get stuck\n\n"
        "Send /start to reset the bot.",
        parse_mode="HTML",
        reply_markup=persistent_reply_keyboard(),
    )


@router.message(Command("menu"))
async def cmd_menu(
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
        action_type="command",
        action_payload="/menu",
    )
