"""Entry point for the Bale ERP marketing bot."""

from __future__ import annotations

import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.activity_logger import ActivityLogger
from bot.config import Settings, create_bot_session
from bot.handlers.router import build_root_router
from bot.menu_state import MenuStateStore
from bot.middlewares import ServicesMiddleware


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        stream=sys.stdout,
    )


async def main() -> None:
    setup_logging()
    logger = logging.getLogger(__name__)

    settings = Settings.from_env()
    activity_logger = ActivityLogger(settings.activity_db_path, settings.activity_log_path)
    await activity_logger.setup()

    session = create_bot_session(settings.api_base_url)
    bot = Bot(
        token=settings.bot_token,
        session=session,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    menu_state = MenuStateStore()

    dp.update.middleware(
        ServicesMiddleware(settings, activity_logger, menu_state)
    )
    dp.include_router(build_root_router())

    logger.info("Starting %s bot (API: %s)", "Bale ERP", settings.api_base_url)
    logger.info("Activity DB: %s", settings.activity_db_path)
    logger.info("Activity log: %s", settings.activity_log_path)

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
