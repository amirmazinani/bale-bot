"""Dependency injection middleware for shared bot services."""

from __future__ import annotations

from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from bot.activity_logger import ActivityLogger
from bot.config import Settings
from bot.menu_state import MenuStateStore


class ServicesMiddleware(BaseMiddleware):
    def __init__(
        self,
        settings: Settings,
        activity_logger: ActivityLogger,
        menu_state: MenuStateStore,
    ) -> None:
        self.settings = settings
        self.activity_logger = activity_logger
        self.menu_state = menu_state

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        data["settings"] = self.settings
        data["activity_logger"] = self.activity_logger
        data["menu_state"] = self.menu_state
        return await handler(event, data)
