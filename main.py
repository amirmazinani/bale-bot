"""Entry point for the Bale ERP marketing bot."""

from __future__ import annotations

import asyncio
import json
import logging
import os
import sys
from typing import Callable

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Update

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


_settings: Settings | None = None
_activity_logger: ActivityLogger | None = None
_bot: Bot | None = None
_dp: Dispatcher | None = None
_menu_state: MenuStateStore | None = None
_initialized = False
_webhook_ready = False


def _init_app() -> None:
    global _settings, _activity_logger, _bot, _dp, _menu_state, _initialized
    if _initialized:
        return

    setup_logging()
    _settings = Settings.from_env()
    _activity_logger = ActivityLogger(_settings.activity_db_path, _settings.activity_log_path)
    asyncio.run(_activity_logger.setup())

    session = create_bot_session(_settings.api_base_url)
    _bot = Bot(
        token=_settings.bot_token,
        session=session,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    _dp = Dispatcher()
    _menu_state = MenuStateStore()

    _dp.update.middleware(ServicesMiddleware(_settings, _activity_logger, _menu_state))
    _dp.include_router(build_root_router())

    _initialized = True


def _ensure_webhook() -> None:
    global _webhook_ready
    if _webhook_ready or _bot is None:
        return

    webhook_url = os.getenv("WEBHOOK_URL")
    if not webhook_url:
        vercel_url = os.getenv("VERCEL_URL")
        if vercel_url:
            webhook_url = f"https://{vercel_url}"

    if not webhook_url:
        logging.getLogger(__name__).warning(
            "WEBHOOK_URL not configured, skipping Telegram webhook registration"
        )
        return

    logging.getLogger(__name__).info("Setting webhook to %s", webhook_url)
    asyncio.run(_bot.set_webhook(webhook_url))
    _webhook_ready = True


async def _handle_update(body: bytes) -> None:
    if not _bot or not _dp:
        raise RuntimeError("Bot or dispatcher not initialized")

    payload = json.loads(body.decode("utf-8"))
    update = Update.model_validate(payload, context={"bot": _bot})
    await _dp.feed_update(_bot, update)


def _wsgi_app(environ: dict[str, str], start_response: Callable) -> list[bytes]:
    _init_app()
    _ensure_webhook()

    method = environ.get("REQUEST_METHOD", "GET")
    if method != "POST":
        start_response("200 OK", [("Content-Type", "text/plain")])
        return [b"Bale bot webhook endpoint"]

    try:
        body_size = int(environ.get("CONTENT_LENGTH", "0") or "0")
    except ValueError:
        body_size = 0

    if body_size > 0:
        body = environ["wsgi.input"].read(body_size)
    else:
        body = environ["wsgi.input"].read()

    try:
        asyncio.run(_handle_update(body))
    except Exception as exc:
        logging.getLogger(__name__).exception("Failed to process incoming update")
        start_response("500 Internal Server Error", [("Content-Type", "text/plain")])
        return [str(exc).encode("utf-8")]

    start_response("200 OK", [("Content-Type", "text/plain")])
    return [b"OK"]


app = _wsgi_app
application = _wsgi_app


async def main() -> None:
    _init_app()
    logger = logging.getLogger(__name__)

    assert _settings is not None
    assert _activity_logger is not None
    assert _bot is not None
    assert _dp is not None
    assert _menu_state is not None

    logger.info("Starting %s bot (API: %s)", "Bale ERP", _settings.api_base_url)
    logger.info("Activity DB: %s", _settings.activity_db_path)
    logger.info("Activity log: %s", _settings.activity_log_path)

    try:
        await _dp.start_polling(_bot, allowed_updates=_dp.resolve_used_update_types())
    finally:
        await _bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
