"""Screen routing: maps callback tokens to text, keyboards, and parent screens."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from aiogram.types import InlineKeyboardMarkup

from bot import callbacks as cb
from bot import callbacks as cb
from bot.content import (
    ABOUT_HTML,
    CONTACT_HTML,
    DEMO_HTML,
    MAIN_MENU_HTML,
    PRICING_HTML,
    PRODUCTS,
    PRODUCTS_MENU_HTML,
    PRODUCT_CALLBACK_TO_KEY,
    WELCOME_HTML,
)
from bot.keyboards import (
    demo_inline,
    main_menu_inline,
    product_detail_inline,
    products_menu_inline,
    subpage_inline,
)

KeyboardFactory = Callable[[], InlineKeyboardMarkup]


@dataclass(frozen=True, slots=True)
class Screen:
    """A navigable bot screen."""

    screen_id: str
    text_html: str
    keyboard_factory: KeyboardFactory
    parent_id: str | None = None
    product_key: str | None = None
    supports_photo: bool = False
    supports_document: bool = False


def _product_screen(callback_token: str) -> Screen:
    product_key = PRODUCT_CALLBACK_TO_KEY[callback_token]
    product = PRODUCTS[product_key]
    return Screen(
        screen_id=callback_token,
        text_html=product.description_html,
        keyboard_factory=lambda pk=product_key: product_detail_inline(pk),
        parent_id=cb.PRODUCTS,
        product_key=product_key,
        supports_photo=product.image_path is not None,
        supports_document=product.brochure_pdf_path is not None,
    )


# Central routing table — extend here when adding new menus.
ROUTES: dict[str, Screen] = {
    "welcome": Screen(
        screen_id="welcome",
        text_html=WELCOME_HTML,
        keyboard_factory=main_menu_inline,
        parent_id=None,
    ),
    cb.MAIN: Screen(
        screen_id=cb.MAIN,
        text_html=MAIN_MENU_HTML,
        keyboard_factory=main_menu_inline,
        parent_id=None,
    ),
    cb.PRODUCTS: Screen(
        screen_id=cb.PRODUCTS,
        text_html=PRODUCTS_MENU_HTML,
        keyboard_factory=products_menu_inline,
        parent_id=cb.MAIN,
    ),
    cb.PRODUCT_CRM: _product_screen(cb.PRODUCT_CRM),
    cb.PRODUCT_TASK: _product_screen(cb.PRODUCT_TASK),
    cb.PRODUCT_INVENTORY: _product_screen(cb.PRODUCT_INVENTORY),
    cb.PRICING: Screen(
        screen_id=cb.PRICING,
        text_html=PRICING_HTML,
        keyboard_factory=lambda: subpage_inline(cb.MAIN),
        parent_id=cb.MAIN,
    ),
    cb.ABOUT: Screen(
        screen_id=cb.ABOUT,
        text_html=ABOUT_HTML,
        keyboard_factory=lambda: subpage_inline(cb.MAIN),
        parent_id=cb.MAIN,
    ),
    cb.DEMO: Screen(
        screen_id=cb.DEMO,
        text_html=DEMO_HTML,
        keyboard_factory=lambda: demo_inline(None),
        parent_id=cb.MAIN,
    ),
    cb.CONTACT: Screen(
        screen_id=cb.CONTACT,
        text_html=CONTACT_HTML,
        keyboard_factory=lambda: subpage_inline(cb.MAIN),
        parent_id=cb.MAIN,
    ),
}


def resolve_demo_screen(product_key: str) -> Screen:
    product = PRODUCTS[product_key]
    return Screen(
        screen_id=cb.demo_for(product_key),
        text_html=(
            f"{DEMO_HTML}\n\n"
            f"<b>Selected product:</b> {product.title}"
        ),
        keyboard_factory=lambda pk=product_key: demo_inline(pk),
        parent_id=cb.PRODUCT_CALLBACK_BY_KEY[product_key],
        product_key=product_key,
    )


def get_screen(route_id: str) -> Screen | None:
    if route_id.startswith("demo:"):
        product_key = route_id.split(":", 1)[1]
        if product_key in PRODUCTS:
            return resolve_demo_screen(product_key)
        return None
    return ROUTES.get(route_id)


def get_parent_route(route_id: str) -> str:
    """Return the immediate parent callback for the Back button."""
    screen = get_screen(route_id)
    if screen and screen.parent_id:
        return screen.parent_id
    return cb.MAIN
