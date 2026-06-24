"""
utils/navigation.py
====================
This module defines the bot's *navigation graph* as plain data, and the
callback_data encoding/decoding scheme used to traverse it.

Design philosophy
------------------
Every inline button the bot ever sends carries a callback_data string of the
form:

    "<route>"                  e.g. "menu:main"
    "<route>:<arg>"             e.g. "product:detail:crm"

We never store "where the user currently is" in a database -- the route
itself, plus a small amount of in-memory FSM state (see utils/fsm.py) for the
demo-request text flow, is enough to know exactly which screen to render.
This makes the bot stateless/restart-safe for all pure-navigation screens:
if the process restarts, old inline buttons still work because the route
string alone fully describes the destination screen.

ROUTES dict
-----------
ROUTES maps a route-key -> a "parent route" key, forming a tree. This is
used by the generic `back_button_for(route)` helper so every screen's
"🔙 Back" button is derived from one declarative table instead of being
hand-wired in every handler (which is how bots get "stuck" navigation bugs).
"""

from __future__ import annotations

from dataclasses import dataclass


# Route key constants -- using constants (not raw strings) avoids typos
# scattered across handler files.
ROUTE_MAIN_MENU = "menu:main"
ROUTE_PRODUCTS_LIST = "menu:products"
ROUTE_PRODUCT_DETAIL = "menu:product_detail"     # requires :<product_key>
ROUTE_PRICING_LIST = "menu:pricing"
ROUTE_PRICING_DETAIL = "menu:pricing_detail"      # requires :<plan_key>
ROUTE_ABOUT = "menu:about"
ROUTE_DEMO_INTRO = "menu:demo_intro"
ROUTE_DEMO_FOR_PRODUCT = "menu:demo_for_product"  # requires :<product_key>
ROUTE_CONTACT = "menu:contact"
ROUTE_BLOG = "menu:blog"

# Lookup table used by content/loader.py to resolve string keys from JSON
# to the canonical route constants above.
ROUTE_MAP: dict[str, str] = {
    "main_menu":        ROUTE_MAIN_MENU,
    "products_list":    ROUTE_PRODUCTS_LIST,
    "product_detail":   ROUTE_PRODUCT_DETAIL,
    "pricing_list":     ROUTE_PRICING_LIST,
    "pricing_detail":   ROUTE_PRICING_DETAIL,
    "about":            ROUTE_ABOUT,
    "demo_intro":       ROUTE_DEMO_INTRO,
    "demo_for_product": ROUTE_DEMO_FOR_PRODUCT,
    "contact":          ROUTE_CONTACT,
    "blog":             ROUTE_BLOG,  # اضافه شده
}

# Parent-route table: child -> parent. ROUTE_MAIN_MENU has no parent (root).
# NOTE: ROUTE_PRODUCT_DETAIL / ROUTE_PRICING_DETAIL are parameterized routes;
# their "back" target is always the corresponding list screen regardless of
# which product/plan was being viewed, which is exactly the desired UX
# ("Back to Products" goes to the product list, not "no-op").
PARENT_ROUTES: dict[str, str] = {
    ROUTE_PRODUCTS_LIST: ROUTE_MAIN_MENU,
    ROUTE_PRODUCT_DETAIL: ROUTE_PRODUCTS_LIST,
    ROUTE_PRICING_LIST: ROUTE_MAIN_MENU,
    ROUTE_PRICING_DETAIL: ROUTE_PRICING_LIST,
    ROUTE_ABOUT: ROUTE_MAIN_MENU,
    ROUTE_DEMO_INTRO: ROUTE_MAIN_MENU,
    ROUTE_DEMO_FOR_PRODUCT: ROUTE_PRODUCT_DETAIL,  # back goes to that product's page
    ROUTE_CONTACT: ROUTE_MAIN_MENU,
    ROUTE_BLOG: ROUTE_MAIN_MENU,  # اضافه شده
}


@dataclass(frozen=True)
class CallbackData:
    """Parsed representation of an inline button's callback_data string."""
    route: str
    arg: str | None = None

    def encode(self) -> str:
        return f"{self.route}:{self.arg}" if self.arg is not None else self.route

    @classmethod
    def decode(cls, raw: str) -> "CallbackData":
        """
        Decode "route:arg" or plain "route" into a CallbackData.

        Routes themselves may contain a colon (e.g. "menu:products"), so we
        split only against the KNOWN route constants rather than naively
        splitting on the first colon. This avoids ambiguity bugs where a
        route name change would silently break parsing.
        """
        for route in sorted(_ALL_ROUTES, key=len, reverse=True):
            if raw == route:
                return cls(route=route, arg=None)
            prefix = route + ":"
            if raw.startswith(prefix):
                return cls(route=route, arg=raw[len(prefix):])
        # Fallback: unknown route. Handlers must treat this defensively.
        return cls(route=raw, arg=None)


_ALL_ROUTES: tuple[str, ...] = (
    ROUTE_MAIN_MENU,
    ROUTE_PRODUCTS_LIST,
    ROUTE_PRODUCT_DETAIL,
    ROUTE_PRICING_LIST,
    ROUTE_PRICING_DETAIL,
    ROUTE_ABOUT,
    ROUTE_DEMO_INTRO,
    ROUTE_DEMO_FOR_PRODUCT,
    ROUTE_CONTACT,
    ROUTE_BLOG,  # اضافه شده
)


def make_callback(route: str, arg: str | None = None) -> str:
    """Convenience builder used by keyboard factories."""
    return CallbackData(route=route, arg=arg).encode()


def parent_of(route: str) -> str:
    """Return the parent route for a given route, defaulting to main menu."""
    return PARENT_ROUTES.get(route, ROUTE_MAIN_MENU)
