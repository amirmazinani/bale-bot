"""
utils/dynamic_navigation.py
===========================
سیستم مسیریابی کاملاً داینامیک که همه چیز از content.json میخونه.

طراحی:
1. همه مسیرها به صورت خودکار از screens در JSON ساخته میشن
2. هر screen که در JSON تعریف شده، یک مسیر به صورت "menu:<screen_key>" دریافت میکنه
3. parentها از parent فیلد در JSON یا به صورت خودکار تعیین میشن
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

# Load content once to build dynamic routes
_CONTENT_PATH = Path(__file__).parent.parent / "content" / "content.json"
_CONTENT_DATA: dict[str, Any] = json.loads(_CONTENT_PATH.read_text(encoding="utf-8"))

# ---------------------------------------------------------------------------
# Dynamic route generation
# ---------------------------------------------------------------------------

def _generate_dynamic_routes() -> tuple[dict[str, str], dict[str, str], dict[str, str]]:
    """
    سه دیکشنری برمیگرداند:
    1. ROUTE_MAP: screen_key -> route_constant
    2. ROUTE_CONSTANTS: route_constant -> route_string
    3. PARENT_ROUTES: child_route -> parent_route
    """
    screens = _CONTENT_DATA.get("screens", {})
    
    # 1. Build ROUTE_MAP and ROUTE_CONSTANTS
    route_map: dict[str, str] = {}
    route_constants: dict[str, str] = {}
    
    for screen_key in screens.keys():
        route_constant = f"ROUTE_{screen_key.upper()}"
        route_string = f"menu:{screen_key}"
        
        route_map[screen_key] = route_constant
        route_constants[route_constant] = route_string
    
    # 2. Build PARENT_ROUTES
    parent_routes: dict[str, str] = {}
    
    for screen_key, screen_data in screens.items():
        route_constant = route_map[screen_key]
        route_string = route_constants[route_constant]
        
        # Check if parent is specified in JSON
        parent_screen = screen_data.get("parent")
        if parent_screen and parent_screen in route_map:
            parent_route_constant = route_map[parent_screen]
            parent_route_string = route_constants[parent_route_constant]
            parent_routes[route_string] = parent_route_string
        else:
            # Default parent is main_menu for non-main screens
            if screen_key != "main_menu" and "main_menu" in route_map:
                parent_routes[route_string] = route_constants[route_map["main_menu"]]
    
    return route_map, route_constants, parent_routes

# Generate routes at module import
ROUTE_MAP, ROUTE_CONSTANTS, PARENT_ROUTES = _generate_dynamic_routes()

# ---------------------------------------------------------------------------
# Create route constants dynamically
# ---------------------------------------------------------------------------

# Add all route constants to module's global namespace
for constant_name, route_string in ROUTE_CONSTANTS.items():
    globals()[constant_name] = route_string

# ---------------------------------------------------------------------------
# CallbackData class (unchanged from original navigation.py)
# ---------------------------------------------------------------------------

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
        splitting on the first colon.
        """
        all_routes = list(ROUTE_CONSTANTS.values())
        
        for route in sorted(all_routes, key=len, reverse=True):
            if raw == route:
                return cls(route=route, arg=None)
            prefix = route + ":"
            if raw.startswith(prefix):
                return cls(route=route, arg=raw[len(prefix):])
        
        # Fallback: unknown route
        return cls(route=raw, arg=None)

# All routes as tuple for easy iteration
ALL_ROUTES: tuple[str, ...] = tuple(ROUTE_CONSTANTS.values())

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def make_callback(route: str, arg: str | None = None) -> str:
    """Convenience builder used by keyboard factories."""
    return CallbackData(route=route, arg=arg).encode()

def parent_of(route: str) -> str:
    """Return the parent route for a given route, defaulting to main menu."""
    main_menu_route = ROUTE_CONSTANTS.get("ROUTE_MAIN_MENU", "menu:main_menu")
    return PARENT_ROUTES.get(route, main_menu_route)

def get_route_for_screen(screen_key: str) -> str | None:
    """Get route string for a screen key."""
    route_constant = ROUTE_MAP.get(screen_key)
    return ROUTE_CONSTANTS.get(route_constant) if route_constant else None

def get_screen_key_for_route(route: str) -> str | None:
    """Get screen key for a route string."""
    # Remove "menu:" prefix
    if route.startswith("menu:"):
        screen_key = route[5:]  # Remove "menu:"
        if screen_key in ROUTE_MAP:
            return screen_key
    return None

# ---------------------------------------------------------------------------
# Export commonly used routes for backward compatibility
# ---------------------------------------------------------------------------

# These will be available as:
# from utils.dynamic_navigation import ROUTE_MAIN_MENU, ROUTE_PRODUCTS_LIST, etc.

# Example usage:
if __name__ == "__main__":
    print("Dynamic Routes Generated:")
    print(f"ROUTE_MAP: {len(ROUTE_MAP)} screens")
    for screen, constant in ROUTE_MAP.items():
        print(f"  {screen} -> {constant} = {ROUTE_CONSTANTS[constant]}")
    
    print(f"\nPARENT_ROUTES: {len(PARENT_ROUTES)} relationships")
    for child, parent in PARENT_ROUTES.items():
        print(f"  {child} -> {parent}")