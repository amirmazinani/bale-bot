"""
content/loader.py
==================
Parses content.json ONCE at import time and exposes typed, ready-to-use
objects.  All InlineKeyboardMarkup objects are pre-built at startup so every
button tap just does a dict lookup — no JSON parsing, no object construction
at request time.

Special button actions:
  "action": "list_products"  → replaced at build time with one button per product
  "action": "list_pricing"   → replaced at build time with one button per plan
  "route":  "<screen_key>"   → callback_data encoded by navigation.make_callback
  "arg":    "<value>"        → optional arg passed alongside the route
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from utils.navigation import make_callback, ROUTE_MAP

_RAW: dict[str, Any] = json.loads(
    (Path(__file__).parent / "content.json").read_text(encoding="utf-8")
)


# ---------------------------------------------------------------------------
# Typed content objects
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Product:
    key: str
    short_title: str
    title: str
    tagline: str
    text: str
    keyboard: InlineKeyboardMarkup
    image_path: str | None = None
    pdf_path: str | None = None


@dataclass(frozen=True)
class PricingPlan:
    key: str
    name: str
    price_label: str
    text: str
    keyboard: InlineKeyboardMarkup


@dataclass(frozen=True)
class Screen:
    text: str
    keyboard: InlineKeyboardMarkup | None = None  # None for text-only screens (e.g. welcome)


# ---------------------------------------------------------------------------
# Keyboard builder
# ---------------------------------------------------------------------------

def _build_keyboard(
    button_rows: list[list[dict]],
    products: dict[str, "Product"] | None = None,
    product_order: list[str] | None = None,
    plans: dict[str, "PricingPlan"] | None = None,
    plan_order: list[str] | None = None,
) -> InlineKeyboardMarkup:
    rows: list[list[InlineKeyboardButton]] = []
    for row in button_rows:
        built_row: list[InlineKeyboardButton] = []
        for btn in row:
            action = btn.get("action")

            if action == "list_products":
                # Expand into one button per product, each in its own row
                for key in (product_order or []):
                    p = (products or {})[key]
                    rows.append([InlineKeyboardButton(
                        text=p.short_title,
                        callback_data=make_callback(ROUTE_MAP["product_detail"], key),
                    )])
                continue  # skip appending to built_row

            if action == "list_pricing":
                for key in (plan_order or []):
                    pl = (plans or {})[key]
                    rows.append([InlineKeyboardButton(
                        text=pl.name,
                        callback_data=make_callback(ROUTE_MAP["pricing_detail"], key),
                    )])
                continue

            route_key = btn.get("route")
            arg = btn.get("arg")
            route = ROUTE_MAP.get(route_key, route_key) if route_key else None
            callback = make_callback(route, arg) if route else None

            url = btn.get("url")

            built_row.append(InlineKeyboardButton(
                text=btn["text"],
                callback_data=callback,
                url=url,
            ))

        if built_row:
            rows.append(built_row)

    return InlineKeyboardMarkup(inline_keyboard=rows)


# ---------------------------------------------------------------------------
# Build everything at import time
# ---------------------------------------------------------------------------

def _build_all() -> tuple[
    dict[str, Product],
    list[str],
    dict[str, PricingPlan],
    list[str],
    dict[str, Screen],
]:
    # --- products (first pass: text + metadata only, keyboard needs plan data) ---
    product_order: list[str] = [p["key"] for p in _RAW["products"]]
    plan_order: list[str] = [p["key"] for p in _RAW["pricing"]]

    # Build plan objects (no dynamic expansion needed)
    plans: dict[str, PricingPlan] = {}
    for p in _RAW["pricing"]:
        plans[p["key"]] = PricingPlan(
            key=p["key"],
            name=p["name"],
            price_label=p["price_label"],
            text=p["text"],
            keyboard=_build_keyboard(p["buttons"]),
        )

    # Build product objects
    products: dict[str, Product] = {}
    for p in _RAW["products"]:
        products[p["key"]] = Product(
            key=p["key"],
            short_title=p["short_title"],
            title=p["title"],
            tagline=p["tagline"],
            text=p["text"],
            image_path=p.get("image_path"),
            pdf_path=p.get("pdf_path"),
            keyboard=_build_keyboard(p["buttons"]),
        )

    # Build static screens
    company = _RAW["company"]
    screens: dict[str, Screen] = {}
    for key, data in _RAW["screens"].items():
        raw_text: str = data["text"]

        # contact screen has {placeholder} variables
        if key == "contact":
            raw_text = raw_text.format(
                company_name=company["name"],
                phone=company["phone"],
                email=company["email"],
                bale_username=company["bale_username"],
                website=company["website"],
            )

        keyboard: InlineKeyboardMarkup | None = None
        if "buttons" in data:
            keyboard = _build_keyboard(
                data["buttons"],
                products=products,
                product_order=product_order,
                plans=plans,
                plan_order=plan_order,
            )

        screens[key] = Screen(text=raw_text, keyboard=keyboard)

    return products, product_order, plans, plan_order, screens


PRODUCTS: dict[str, Product]
PRODUCT_ORDER: list[str]
PRICING_PLANS: dict[str, PricingPlan]
PRICING_ORDER: list[str]
SCREENS: dict[str, Screen]

PRODUCTS, PRODUCT_ORDER, PRICING_PLANS, PRICING_ORDER, SCREENS = _build_all()

# Convenience aliases for commonly accessed strings
COMPANY: dict[str, str] = _RAW["company"]
REPLY_KEYBOARD_BUTTONS: list[dict] = _RAW["reply_keyboard"]["buttons"]
