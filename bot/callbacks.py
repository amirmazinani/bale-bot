"""Compact callback_data tokens (Bale limit: 1–64 bytes per button)."""

from __future__ import annotations

# Navigation screens
MAIN = "nav:main"
PRODUCTS = "nav:products"
PRICING = "nav:pricing"
ABOUT = "nav:about"
DEMO = "nav:demo"
CONTACT = "nav:contact"

# Product detail screens
PRODUCT_CRM = "prod:crm"
PRODUCT_TASK = "prod:task"
PRODUCT_INVENTORY = "prod:inv"

PRODUCT_CALLBACK_BY_KEY: dict[str, str] = {
    "crm": PRODUCT_CRM,
    "task": PRODUCT_TASK,
    "inv": PRODUCT_INVENTORY,
}


def demo_for(product_key: str) -> str:
    return f"demo:{product_key}"


# Reply-keyboard labels (must match handlers)
REPLY_MAIN_MENU = "🏠 Main Menu"
REPLY_CONTACT = "📞 Contact / Support"
