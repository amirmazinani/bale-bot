"""
keyboards/inline.py
=====================
Every inline keyboard in the bot is built here, as a small pure function
per screen. Keeping them pure (input -> InlineKeyboardMarkup, no I/O) makes
them trivially unit-testable and keeps handlers focused on orchestration
rather than markup construction.

Each factory uses utils.navigation.make_callback() to build callback_data,
and ends (where applicable) with a "🔙 Back" button computed from the
navigation graph -- so adding a brand-new screen later just means adding one
new factory function + one line in PARENT_ROUTES, not re-wiring back-buttons
by hand everywhere.
"""

from __future__ import annotations

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from content.erp_content import PRICING_ORDER, PRICING_PLANS, PRODUCT_ORDER, PRODUCTS
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
    make_callback,
)


def _back_button(route: str, arg: str | None = None, label: str = "🔙 بازگشت") -> InlineKeyboardButton:
    return InlineKeyboardButton(text=label, callback_data=make_callback(route, arg))


def _main_menu_button() -> InlineKeyboardButton:
    return InlineKeyboardButton(text="🏠 منو اصلی", callback_data=make_callback(ROUTE_MAIN_MENU))


# ---------------------------------------------------------------------------
# Main menu
# ---------------------------------------------------------------------------

def main_menu_keyboard() -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text="📦 محصولات ما", callback_data=make_callback(ROUTE_PRODUCTS_LIST))],
        [InlineKeyboardButton(text="💰 پلن‌ها", callback_data=make_callback(ROUTE_PRICING_LIST))],
        [InlineKeyboardButton(text="🏢 درباره ما", callback_data=make_callback(ROUTE_ABOUT))],
        [InlineKeyboardButton(text="🚀 درخواست نمایش دمو", callback_data=make_callback(ROUTE_DEMO_INTRO))],
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


# ---------------------------------------------------------------------------
# Products
# ---------------------------------------------------------------------------

def products_list_keyboard() -> InlineKeyboardMarkup:
    rows = []
    for key in PRODUCT_ORDER:
        product = PRODUCTS[key]
        rows.append([
            InlineKeyboardButton(
                text=product.short_title,
                callback_data=make_callback(ROUTE_PRODUCT_DETAIL, key),
            )
        ])
    rows.append([_main_menu_button()])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def product_detail_keyboard(product_key: str) -> InlineKeyboardMarkup:
    rows = [
        [
            InlineKeyboardButton(
                text="🚀 درخواست نمایش دمو برای این محصول",
                callback_data=make_callback(ROUTE_DEMO_FOR_PRODUCT, product_key),
            )
        ],
        [_back_button(ROUTE_PRODUCTS_LIST, label="🔙 بازگشت به محصولات")],
        [_main_menu_button()],
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


# ---------------------------------------------------------------------------
# Pricing
# ---------------------------------------------------------------------------

def pricing_list_keyboard() -> InlineKeyboardMarkup:
    rows = []
    for key in PRICING_ORDER:
        plan = PRICING_PLANS[key]
        rows.append([
            InlineKeyboardButton(
                text=plan.name,
                callback_data=make_callback(ROUTE_PRICING_DETAIL, key),
            )
        ])
    rows.append([_main_menu_button()])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def pricing_detail_keyboard() -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text="🚀 درخواست نمایش دمو", callback_data=make_callback(ROUTE_DEMO_INTRO))],
        [_back_button(ROUTE_PRICING_LIST, label="🔙 بازگشت به پلن‌ها")],
        [_main_menu_button()],
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


# ---------------------------------------------------------------------------
# About Us
# ---------------------------------------------------------------------------

def about_keyboard() -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text="📦 محصولات ما", callback_data=make_callback(ROUTE_PRODUCTS_LIST))],
        [_main_menu_button()],
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


# ---------------------------------------------------------------------------
# Demo request
# ---------------------------------------------------------------------------

def demo_intro_keyboard() -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text="📞 رد شدن — مشاهده اطلاعات تماس", callback_data=make_callback(ROUTE_CONTACT))],
        [_main_menu_button()],
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def demo_for_product_keyboard(product_key: str) -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text="📞 رد شدن — مشاهده اطلاعات تماس", callback_data=make_callback(ROUTE_CONTACT))],
        [_back_button(ROUTE_PRODUCT_DETAIL, product_key, label="🔙 بازگشت به محصول")],
        [_main_menu_button()],
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def demo_thankyou_keyboard() -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text="📦 محصولات ما", callback_data=make_callback(ROUTE_PRODUCTS_LIST))],
        [_main_menu_button()],
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


# ---------------------------------------------------------------------------
# Contact
# ---------------------------------------------------------------------------

def contact_keyboard() -> InlineKeyboardMarkup:
    rows = [[_main_menu_button()]]
    return InlineKeyboardMarkup(inline_keyboard=rows)
