"""Reply and inline keyboard builders."""

from __future__ import annotations

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from bot import callbacks as cb
from bot.content import PRODUCTS


def persistent_reply_keyboard() -> ReplyKeyboardMarkup:
    """Bottom menu always visible: Main Menu + Contact."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=cb.REPLY_MAIN_MENU),
                KeyboardButton(text=cb.REPLY_CONTACT),
            ],
        ],
        resize_keyboard=True,
        is_persistent=True,
        input_field_placeholder="Choose from the menu below…",
    )


def main_menu_inline() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📦 Our Products", callback_data=cb.PRODUCTS)],
            [InlineKeyboardButton(text="💰 Pricing Plans", callback_data=cb.PRICING)],
            [InlineKeyboardButton(text="🏢 About Us", callback_data=cb.ABOUT)],
            [InlineKeyboardButton(text="🚀 Request a Demo", callback_data=cb.DEMO)],
        ]
    )


def products_menu_inline() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Customer Relationship Management (CRM)",
                    callback_data=cb.PRODUCT_CRM,
                )
            ],
            [
                InlineKeyboardButton(
                    text="Task & Project Management",
                    callback_data=cb.PRODUCT_TASK,
                )
            ],
            [
                InlineKeyboardButton(
                    text="Inventory/Finance System",
                    callback_data=cb.PRODUCT_INVENTORY,
                )
            ],
            [
                InlineKeyboardButton(text="🔙 Back", callback_data=cb.MAIN),
                InlineKeyboardButton(text="🏠 Main Menu", callback_data=cb.MAIN),
            ],
        ]
    )


def product_detail_inline(product_key: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🚀 Request Demo for this Product",
                    callback_data=cb.demo_for(product_key),
                )
            ],
            [
                InlineKeyboardButton(text="🔙 Back to Products", callback_data=cb.PRODUCTS),
                InlineKeyboardButton(text="🏠 Main Menu", callback_data=cb.MAIN),
            ],
        ]
    )


def subpage_inline(back_callback: str = cb.MAIN) -> InlineKeyboardMarkup:
    """Standard back navigation for pricing, about, demo, contact."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🔙 Back", callback_data=back_callback),
                InlineKeyboardButton(text="🏠 Main Menu", callback_data=cb.MAIN),
            ],
        ]
    )


def demo_inline(product_key: str | None = None) -> InlineKeyboardMarkup:
    """Demo confirmation with contextual back target."""
    if product_key:
        back_target = cb.PRODUCT_CALLBACK_BY_KEY[product_key]
    else:
        back_target = cb.MAIN
    rows: list[list[InlineKeyboardButton]] = [
        [
            InlineKeyboardButton(text="🔙 Back", callback_data=back_target),
            InlineKeyboardButton(text="🏠 Main Menu", callback_data=cb.MAIN),
        ],
    ]
    if product_key:
        product = PRODUCTS[product_key]
        product_callback = cb.PRODUCT_CALLBACK_BY_KEY[product_key]
        rows.insert(
            0,
            [
                InlineKeyboardButton(
                    text=f"📦 {product.short_label}",
                    callback_data=product_callback,
                )
            ],
        )
    return InlineKeyboardMarkup(inline_keyboard=rows)
