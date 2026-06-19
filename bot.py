"""
bot.py
======
Application entrypoint. Run with:

    python bot.py

Responsibilities:
  1. Configure logging.
  2. Build the Bot instance pointed at Bale's API (bot_instance.py).
  3. Assemble the Dispatcher with routers in a DELIBERATE order (this
     matters! see comments below).
  4. Start polling (default) or a webhook server, based on config.

Router order matters
---------------------
aiogram routers are checked in registration order, and within a router,
handlers are checked top-to-bottom; the FIRST matching handler wins and
stops propagation by default. We register:

    1. start_router        -- /start command (most specific: a command)
    2. reply_menu_router    -- exact-text matches on the 2 persistent buttons
    3. demo_capture_router  -- free text, but ONLY while FSM says "awaiting
                                demo info" (guarded by a custom filter)
    4. menu_router          -- ALL CallbackQuery (inline button) taps
    5. fallback_router      -- anything else (must be LAST, it's a catch-all)

If fallback_router were registered before demo_capture_router, it would
swallow every demo-info text reply before demo_capture_router ever saw it --
exactly the kind of subtle ordering bug worth documenting explicitly.
"""

from __future__ import annotations

import asyncio
import logging

from aiogram import Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from bot_instance import build_bot
from config import settings
from handlers import demo_capture, fallback, menu_router, reply_menu, start
from utils.logging_setup import configure_logging

logger = logging.getLogger(__name__)


def build_dispatcher() -> Dispatcher:
    dp = Dispatcher()
    dp.include_router(start.router)
    dp.include_router(reply_menu.router)
    dp.include_router(demo_capture.router)
    dp.include_router(menu_router.router)
    dp.include_router(fallback.router)  # must stay last
    return dp


async def _run_polling() -> None:
    bot = build_bot()
    dp = build_dispatcher()
    logger.info("Starting bot in LONG POLLING mode against %s", settings.API_BASE_URL_TEMPLATE)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


async def _run_webhook() -> None:
    bot = build_bot()
    dp = build_dispatcher()

    webhook_url = settings.WEBHOOK_HOST.rstrip("/") + settings.WEBHOOK_PATH
    logger.info("Starting bot in WEBHOOK mode. Setting webhook to %s", webhook_url)
    await bot.set_webhook(webhook_url, drop_pending_updates=True)

    app = web.Application()
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=settings.WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, settings.WEBAPP_HOST, settings.WEBAPP_PORT)
    await site.start()
    logger.info("Webhook server listening on %s:%s", settings.WEBAPP_HOST, settings.WEBAPP_PORT)

    # Keep the process alive.
    try:
        await asyncio.Event().wait()
    finally:
        await runner.cleanup()


def main() -> None:
    configure_logging(settings.LOG_DIR, settings.LOG_LEVEL, settings.LOG_TO_FILE)
    logger.info("=== %s ERP Bot starting up ===", settings.COMPANY_NAME)

    if settings.BOT_TOKEN.startswith("PUT_YOUR"):
        logger.warning(
            "BALE_BOT_TOKEN is not set! Set the BALE_BOT_TOKEN environment "
            "variable before running in production."
        )

    try:
        if settings.USE_WEBHOOK:
            asyncio.run(_run_webhook())
        else:
            asyncio.run(_run_polling())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped by user/system signal.")


if __name__ == "__main__":
    main()
