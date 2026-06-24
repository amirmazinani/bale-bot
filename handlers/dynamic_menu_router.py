"""
handlers/dynamic_menu_router.py
===============================
سیستم رندر کاملاً داینامیک که همه صفحات از content.json رو به صورت خودکار هندل میکنه.

طراحی:
1. یک هندلر اصلی که همه routeها رو هندل میکنه
2. هر صفحه به صورت خودکار از SCREENS رندر میشه
3. نیاز به تعریف رندرر جداگانه نداره
"""

from __future__ import annotations

import logging
from typing import Awaitable, Callable

from aiogram import Router
from aiogram.types import CallbackQuery

from content.loader import SCREENS
from utils.dynamic_navigation import CallbackData, get_screen_key_for_route
from utils.fsm import fsm_store
from utils.screen import render_screen, safe_answer_callback

logger = logging.getLogger(__name__)
router = Router(name="dynamic_menu_router")

RendererT = Callable[[CallbackQuery, str | None], Awaitable[None]]

# ---------------------------------------------------------------------------
# Generic renderer for ALL screens
# ---------------------------------------------------------------------------

async def _render_generic_screen(callback: CallbackQuery, arg: str | None) -> None:
    """
    رندرر عمومی برای همه صفحات.
    
    کارکرد:
    1. route رو به screen key تبدیل میکنه
    2. صفحه رو از SCREENS میخونه
    3. اون رو رندر میکنه
    """
    if callback.data is None:
        return
    
    parsed = CallbackData.decode(callback.data)
    screen_key = get_screen_key_for_route(parsed.route)
    
    if not screen_key:
        logger.warning("No screen key found for route=%r", parsed.route)
        # Fallback to main menu
        screen_key = "main_menu"
    
    # Handle special screens that need FSM reset
    if screen_key == "main_menu":
        fsm_store.reset(callback.message.chat.id)
    
    # Get screen from loader
    screen = SCREENS.get(screen_key)
    
    if not screen:
        logger.error("Screen not found in SCREENS: %r", screen_key)
        # Try to fallback to main menu
        screen = SCREENS.get("main_menu")
        if not screen:
            await safe_answer_callback(callback)
            return
    
    # Render the screen
    await render_screen(callback, screen.text, screen.keyboard)

# ---------------------------------------------------------------------------
# Specialized renderers for complex screens
# ---------------------------------------------------------------------------

async def _render_product_detail(callback: CallbackQuery, arg: str | None) -> None:
    """
    رندرر تخصصی برای صفحات محصول.
    این نیاز به منطق خاص داره برای نمایش عکس و ...
    """
    from content.loader import PRODUCTS
    from config import settings
    
    product = PRODUCTS.get(arg or "")
    if product is None:
        logger.warning("Unknown product key in callback: %r", arg)
        # Fallback to products list
        screen = SCREENS.get("products_list")
        if screen:
            await render_screen(callback, screen.text, screen.keyboard)
        return
    
    # Send image if available
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
    
    # Render product detail
    await render_screen(callback, product.text, product.keyboard)

async def _render_pricing_detail(callback: CallbackQuery, arg: str | None) -> None:
    """
    رندرر تخصصی برای صفحات قیمت.
    """
    from content.loader import PRICING_PLANS
    
    plan = PRICING_PLANS.get(arg or "")
    if plan is None:
        logger.warning("Unknown pricing plan key in callback: %r", arg)
        # Fallback to pricing list
        screen = SCREENS.get("pricing_list")
        if screen:
            await render_screen(callback, screen.text, screen.keyboard)
        return
    
    await render_screen(callback, plan.text, plan.keyboard)

async def _render_demo_intro(callback: CallbackQuery, arg: str | None) -> None:
    """
    رندرر تخصصی برای صفحه درخواست دمو.
    """
    fsm_store.set_awaiting_demo_info(callback.message.chat.id, product_key=None)
    screen = SCREENS.get("demo_intro")
    if screen:
        await render_screen(callback, screen.text, screen.keyboard)

async def _render_demo_for_product(callback: CallbackQuery, arg: str | None) -> None:
    """
    رندرر تخصصی برای درخواست دمو محصول خاص.
    """
    from content.loader import PRODUCTS
    
    product = PRODUCTS.get(arg or "")
    if product is None:
        await _render_demo_intro(callback, None)
        return
    
    fsm_store.set_awaiting_demo_info(callback.message.chat.id, product_key=arg)
    screen = SCREENS.get("demo_intro")
    if screen:
        text = f"{product.title}\\n\\n" + screen.text.split("\\n\\n", 1)[-1]
        await render_screen(callback, text, product.keyboard)

# ---------------------------------------------------------------------------
# Dynamic route handler dispatch
# ---------------------------------------------------------------------------

def _get_renderer_for_route(route: str) -> RendererT:
    """
    انتخاب رندرر مناسب بر اساس route.
    
    منطق:
    1. برای routeهای خاص، رندرر تخصصی
    2. برای بقیه، رندرر عمومی
    """
    # Map specific routes to specialized renderers
    specialized_routes = {
        "menu:product_detail": _render_product_detail,
        "menu:pricing_detail": _render_pricing_detail,
        "menu:demo_intro": _render_demo_intro,
        "menu:demo_for_product": _render_demo_for_product,
    }
    
    return specialized_routes.get(route, _render_generic_screen)

# ---------------------------------------------------------------------------
# Main handler - handles ALL routes dynamically
# ---------------------------------------------------------------------------

@router.callback_query()
async def on_any_inline_callback(callback: CallbackQuery) -> None:
    """
    هندلر اصلی برای همه callbackهای inline.
    
    همه routeها رو به صورت داینامیک هندل میکنه.
    """
    if callback.data is None:
        await safe_answer_callback(callback)
        return
    
    parsed = CallbackData.decode(callback.data)
    user_id = callback.from_user.id if callback.from_user else "unknown"
    logger.info("user_id=%s tapped route=%s arg=%s", user_id, parsed.route, parsed.arg)
    
    # Get the appropriate renderer
    renderer = _get_renderer_for_route(parsed.route)
    await safe_answer_callback(callback)  # stop the spinner immediately
    
    if renderer is None:
        logger.warning("No renderer found for route=%r; falling back to generic.", parsed.route)
        await _render_generic_screen(callback, parsed.arg)
        return
    
    try:
        await renderer(callback, parsed.arg)
    except Exception as e:
        logger.exception("Error rendering route=%s arg=%s: %s", parsed.route, parsed.arg, e)
        # Fallback to main menu on error
        screen = SCREENS.get("main_menu")
        if screen:
            await render_screen(callback, screen.text, screen.keyboard)