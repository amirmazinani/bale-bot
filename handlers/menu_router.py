"""
handlers/menu_router.py
=========================
This is the central nervous system of the bot: ONE CallbackQuery handler
that receives every inline button tap, decodes its route via
utils.navigation.CallbackData, and dispatches to a small renderer function
via the ROUTE_HANDLERS dispatch table at the bottom of this file.

Why one handler + a dispatch dict instead of N separate @router.callback_query
decorators per route? Two reasons:
  1. It makes the full menu tree visible in one place (the dict literal),
     which doubles as living documentation of "every screen the bot has".
  2. Cross-cutting concerns (logging every navigation event, always calling
     safe_answer_callback) happen exactly once, not duplicated N times.

Each renderer has the signature:
    async def renderer(callback: CallbackQuery, arg: str | None) -> None
"""

from __future__ import annotations

import logging
from typing import Awaitable, Callable

from aiogram import Router
from aiogram.types import CallbackQuery

from config import settings
from content.loader import PRICING_PLANS, PRODUCTS, SCREENS
from utils.fsm import fsm_store
from utils.navigation import (
    ROUTE_ABOUT,
    ROUTE_BLOG,           # اضافه شده
    ROUTE_CONTACT,
    ROUTE_DEMO_FOR_PRODUCT,
    ROUTE_DEMO_INTRO,
    ROUTE_MAIN_MENU,
    ROUTE_PRICING_DETAIL,
    ROUTE_PRICING_LIST,
    ROUTE_PRODUCT_DETAIL,
    ROUTE_PRODUCTS_LIST,
    CallbackData,
)
from utils.screen import render_screen, safe_answer_callback

logger = logging.getLogger(__name__)
router = Router(name="menu_router")

RendererT = Callable[[CallbackQuery, str | None], Awaitable[None]]


# ---------------------------------------------------------------------------
# Individual screen renderers
# ---------------------------------------------------------------------------

async def _render_main_menu(callback: CallbackQuery, arg: str | None) -> None:
    fsm_store.reset(callback.message.chat.id)
    s = SCREENS["main_menu"]
    await render_screen(callback, s.text, s.keyboard)


async def _render_products_list(callback: CallbackQuery, arg: str | None) -> None:
    s = SCREENS["products_list"]
    await render_screen(callback, s.text, s.keyboard)


async def _render_product_detail(callback: CallbackQuery, arg: str | None) -> None:
    product = PRODUCTS.get(arg or "")
    if product is None:
        logger.warning("Unknown product key in callback: %r", arg)
        await _render_products_list(callback, None)
        return

    image_path = settings.ASSETS_DIR.parent / product.image_path if product.image_path else None
    if image_path and image_path.exists():
        try:
            from aiogram.types import FSInputFile
            await callback.message.answer_photo(
                FSInputFile(str(image_path)),
                caption=product.title,
            )
        except Exception:
            logger.exception("Failed to send promo image for product=%s", arg)

    await render_screen(callback, product.text, product.keyboard)


async def _render_pricing_list(callback: CallbackQuery, arg: str | None) -> None:
    s = SCREENS["pricing_list"]
    await render_screen(callback, s.text, s.keyboard)


async def _render_pricing_detail(callback: CallbackQuery, arg: str | None) -> None:
    plan = PRICING_PLANS.get(arg or "")
    if plan is None:
        logger.warning("پلن قیمت‌گذاری ناشناخته در callback: %r", arg)
        await _render_pricing_list(callback, None)
        return
    await render_screen(callback, plan.text, plan.keyboard)


async def _render_about(callback: CallbackQuery, arg: str | None) -> None:
    s = SCREENS["about"]
    await render_screen(callback, s.text, s.keyboard)


async def _render_demo_intro(callback: CallbackQuery, arg: str | None) -> None:
    fsm_store.set_awaiting_demo_info(callback.message.chat.id, product_key=None)
    s = SCREENS["demo_intro"]
    await render_screen(callback, s.text, s.keyboard)


async def _render_demo_for_product(callback: CallbackQuery, arg: str | None) -> None:
    product = PRODUCTS.get(arg or "")
    if product is None:
        await _render_demo_intro(callback, None)
        return
    fsm_store.set_awaiting_demo_info(callback.message.chat.id, product_key=arg)
    s = SCREENS["demo_intro"]
    text = f"{product.title}\n\n" + s.text.split("\n\n", 1)[-1]
    await render_screen(callback, text, product.keyboard)


async def _render_contact(callback: CallbackQuery, arg: str | None) -> None:
    fsm_store.reset(callback.message.chat.id)
    s = SCREENS["contact"]
    await render_screen(callback, s.text, s.keyboard)


async def _render_blog(callback: CallbackQuery, arg: str | None) -> None:
    """رندر صفحه وبلاگ"""
    s = SCREENS["blog"]
    await render_screen(callback, s.text, s.keyboard)


# ---------------------------------------------------------------------------
# Dispatch table: route -> renderer
# ---------------------------------------------------------------------------

ROUTE_HANDLERS: dict[str, RendererT] = {
    ROUTE_MAIN_MENU: _render_main_menu,
    ROUTE_PRODUCTS_LIST: _render_products_list,
    ROUTE_PRODUCT_DETAIL: _render_product_detail,
    ROUTE_PRICING_LIST: _render_pricing_list,
    ROUTE_PRICING_DETAIL: _render_pricing_detail,
    ROUTE_ABOUT: _render_about,
    ROUTE_DEMO_INTRO: _render_demo_intro,
    ROUTE_DEMO_FOR_PRODUCT: _render_demo_for_product,
    ROUTE_CONTACT: _render_contact,
    ROUTE_BLOG: _render_blog,  # اضافه شده
}


@router.callback_query()
async def on_any_inline_callback(callback: CallbackQuery) -> None:
    """
    Single entry point for ALL inline keyboard taps in the bot.

    Decodes callback.data into a CallbackData(route, arg), looks up the
    matching renderer, and runs it. Unknown routes (e.g. a stale button
    from a previous bot version) fall back safely to the main menu instead
    of leaving the user with a dead button.
    """
    if callback.data is None:
        await safe_answer_callback(callback)
        return

    parsed = CallbackData.decode(callback.data)
    user_id = callback.from_user.id if callback.from_user else "unknown"
    logger.info("user_id=%s tapped route=%s arg=%s", user_id, parsed.route, parsed.arg)

    renderer = ROUTE_HANDLERS.get(parsed.route)
    await safe_answer_callback(callback)  # stop the spinner immediately

    if renderer is None:
        logger.warning("No renderer registered for route=%r; falling back to main menu.", parsed.route)
        await _render_main_menu(callback, None)
        return

    await renderer(callback, parsed.arg)
