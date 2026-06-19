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
from content.erp_content import (
    ABOUT_US_HTML,
    DEMO_INTRO_HTML,
    MAIN_MENU_PROMPT_HTML,
    PRICING_PLANS,
    PRODUCTS,
    contact_html,
)
from keyboards.inline import (
    about_keyboard,
    contact_keyboard,
    demo_for_product_keyboard,
    demo_intro_keyboard,
    main_menu_keyboard,
    pricing_detail_keyboard,
    pricing_list_keyboard,
    product_detail_keyboard,
    products_list_keyboard,
)
from utils.fsm import fsm_store
from utils.navigation import (
    ROUTE_ABOUT,
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
    await render_screen(callback, MAIN_MENU_PROMPT_HTML, main_menu_keyboard())


async def _render_products_list(callback: CallbackQuery, arg: str | None) -> None:
    await render_screen(callback, "<b>📦 Our Products</b>\nChoose a module to learn more:", products_list_keyboard())


async def _render_product_detail(callback: CallbackQuery, arg: str | None) -> None:
    product = PRODUCTS.get(arg or "")
    if product is None:
        logger.warning("Unknown product key in callback: %r", arg)
        await _render_products_list(callback, None)
        return

    # --- Rich content placeholder -------------------------------------
    # If a promo image exists on disk, send it as its own message right
    # before the detail card. This keeps the *editable* text card intact
    # (you cannot edit a text message into a photo message in-place), while
    # still feeling like "one screen" because it arrives immediately before.
    image_path = settings.ASSETS_DIR.parent / product.image_path if product.image_path else None
    if image_path and image_path.exists():
        try:
            from aiogram.types import FSInputFile
            await callback.message.answer_photo(
                FSInputFile(str(image_path)),
                caption=f"{product.title} — promotional overview",
            )
        except Exception:
            logger.exception("Failed to send promo image for product=%s", arg)
    # else: no-op. Placeholder wiring only -- ship your real assets at the
    # path declared in content/erp_content.py (Product.image_path) and this
    # activates automatically with no code changes.

    await render_screen(callback, product.description_html, product_detail_keyboard(arg))


async def _render_pricing_list(callback: CallbackQuery, arg: str | None) -> None:
    await render_screen(
        callback,
        "<b>💰 Pricing Plans</b>\nChoose a plan to see what's included:",
        pricing_list_keyboard(),
    )


async def _render_pricing_detail(callback: CallbackQuery, arg: str | None) -> None:
    plan = PRICING_PLANS.get(arg or "")
    if plan is None:
        logger.warning("Unknown pricing plan key in callback: %r", arg)
        await _render_pricing_list(callback, None)
        return
    await render_screen(callback, plan.summary_html, pricing_detail_keyboard())


async def _render_about(callback: CallbackQuery, arg: str | None) -> None:
    await render_screen(callback, ABOUT_US_HTML, about_keyboard())


async def _render_demo_intro(callback: CallbackQuery, arg: str | None) -> None:
    fsm_store.set_awaiting_demo_info(callback.message.chat.id, product_key=None)
    await render_screen(callback, DEMO_INTRO_HTML, demo_intro_keyboard())


async def _render_demo_for_product(callback: CallbackQuery, arg: str | None) -> None:
    product = PRODUCTS.get(arg or "")
    if product is None:
        await _render_demo_intro(callback, None)
        return
    fsm_store.set_awaiting_demo_info(callback.message.chat.id, product_key=arg)
    text = (
        f"<b>🚀 Request a Demo — {product.title}</b>\n\n"
        "Please reply with your <b>full name</b>, <b>company name</b>, and "
        "<b>phone number</b> in a single message, for example:\n"
        "<code>Jane Doe, Acme Co, +98 912 000 0000</code>\n\n"
        "Or tap a button below."
    )
    await render_screen(callback, text, demo_for_product_keyboard(arg))


async def _render_contact(callback: CallbackQuery, arg: str | None) -> None:
    fsm_store.reset(callback.message.chat.id)
    text = contact_html(
        settings.COMPANY_NAME,
        settings.SUPPORT_PHONE,
        settings.SUPPORT_EMAIL,
        settings.SALES_BALE_USERNAME,
        settings.COMPANY_WEBSITE,
    )
    await render_screen(callback, text, contact_keyboard())


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
