"""
content/erp_content.py
=======================
This module is the single source of truth for ALL text content shown by the
bot: product descriptions, pricing plans, company info, demo flow copy.

Why a dedicated content module instead of inlining strings in handlers?
  1. Non-developers (e.g. a marketing person) can edit this one file safely.
  2. Handlers stay clean: they fetch content by key and render it.
  3. It mirrors what a CMS/admin-panel would give you, but hardcoded as
     requested -- no DB, no external API calls, no admin panel.

Formatting:
  Bale, like Telegram, supports a constrained HTML subset for message
  formatting (b, i, u, s, code, pre, a, etc.). We use HTML mode everywhere
  (parse_mode="HTML") because it is more forgiving with special characters
  than MarkdownV2 (no need to escape '.', '-', '!' etc.), which matters a
  lot for Persian/Farsi text and prices.
"""

from __future__ import annotations

from dataclasses import dataclass


# ---------------------------------------------------------------------------
# Products
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Product:
    key: str               # internal id used in callback_data, e.g. "crm"
    short_title: str       # shown on the product-list inline button
    title: str             # full title shown on the detail page
    tagline: str
    description_html: str  # full HTML-formatted body for the detail page
    image_path: str | None = None   # local file path placeholder for promo image
    pdf_path: str | None = None     # local file path placeholder for feature-list PDF


PRODUCTS: dict[str, Product] = {
    "crm": Product(
        key="crm",
        short_title="Customer Relationship Management (CRM)",
        title="📇 NovaERP CRM",
        tagline="Know every customer. Close every deal.",
        description_html=(
            "<b>📇 NovaERP CRM</b>\n"
            "<i>Know every customer. Close every deal.</i>\n\n"
            "Our CRM module centralizes every customer interaction so your "
            "sales and support teams always work from the same source of truth.\n\n"
            "<b>Key Features:</b>\n"
            "• 🧾 360° customer profiles &amp; interaction timeline\n"
            "• 🎯 Visual sales pipeline with drag-and-drop deal stages\n"
            "• 📞 Call, email &amp; meeting logging with auto-reminders\n"
            "• 🤖 Lead scoring and automatic lead assignment rules\n"
            "• 📊 Real-time sales dashboards and forecast reports\n"
            "• 🔗 Two-way sync with the Task &amp; Project Management module\n\n"
            "<b>Best for:</b> Sales teams, account managers, and customer "
            "success teams who need one shared pipeline view.\n"
        ),
        image_path="assets/crm_promo.png",
        pdf_path="assets/crm_features.pdf",
    ),
    "tasks": Product(
        key="tasks",
        short_title="Task & Project Management",
        title="🗂 NovaERP Task & Project Management",
        tagline="Plan it, track it, ship it -- on time.",
        description_html=(
            "<b>🗂 NovaERP Task &amp; Project Management</b>\n"
            "<i>Plan it, track it, ship it -- on time.</i>\n\n"
            "Coordinate teams and projects from kickoff to delivery, with "
            "full visibility for managers and a clean, simple board for "
            "everyone doing the work.\n\n"
            "<b>Key Features:</b>\n"
            "• 📋 Kanban boards, Gantt charts, and list views\n"
            "• ⏱ Time tracking &amp; workload balancing per teammate\n"
            "• 🔁 Recurring tasks and dependency chains\n"
            "• 🔔 Smart deadline notifications and escalations\n"
            "• 🧩 Custom fields, tags, and project templates\n"
            "• 🔗 Native integration with the CRM module for client projects\n\n"
            "<b>Best for:</b> Operations, product, and project teams running "
            "multiple concurrent projects.\n"
        ),
        image_path="assets/tasks_promo.png",
        pdf_path="assets/tasks_features.pdf",
    ),
    "finance": Product(
        key="finance",
        short_title="Inventory / Finance System",
        title="💼 NovaERP Inventory & Finance",
        tagline="Stock, invoices, and cash flow -- unified.",
        description_html=(
            "<b>💼 NovaERP Inventory &amp; Finance System</b>\n"
            "<i>Stock, invoices, and cash flow -- unified.</i>\n\n"
            "Manage warehouses, purchasing, and accounting in one connected "
            "system so your numbers are always accurate and up to date.\n\n"
            "<b>Key Features:</b>\n"
            "• 📦 Multi-warehouse inventory with real-time stock levels\n"
            "• 🧮 Automated invoicing, billing &amp; tax calculation\n"
            "• 💳 Accounts payable/receivable and bank reconciliation\n"
            "• 📈 Profit &amp; loss, balance sheet, and cash-flow reports\n"
            "• 🛒 Purchase orders with supplier management\n"
            "• 🔗 Auto-sync of sales orders from the CRM module\n\n"
            "<b>Best for:</b> Finance teams, warehouse managers, and business "
            "owners who need a single financial source of truth.\n"
        ),
        image_path="assets/finance_promo.png",
        pdf_path="assets/finance_features.pdf",
    ),
}

PRODUCT_ORDER: list[str] = ["crm", "tasks", "finance"]


# ---------------------------------------------------------------------------
# Pricing
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class PricingPlan:
    key: str
    name: str
    price_label: str
    summary_html: str


PRICING_PLANS: dict[str, PricingPlan] = {
    "starter": PricingPlan(
        key="starter",
        name="🌱 Starter",
        price_label="Contact us for pricing",
        summary_html=(
            "<b>🌱 Starter Plan</b>\n\n"
            "Designed for small teams (up to 10 users) getting started with ERP.\n\n"
            "<b>Includes:</b>\n"
            "• CRM <i>or</i> Task Management module (choose one)\n"
            "• Up to 10 user seats\n"
            "• Email support (business hours)\n"
            "• Monthly product updates\n"
        ),
    ),
    "professional": PricingPlan(
        key="professional",
        name="🚀 Professional",
        price_label="Contact us for pricing",
        summary_html=(
            "<b>🚀 Professional Plan</b>\n\n"
            "For growing companies that need multiple modules working together.\n\n"
            "<b>Includes:</b>\n"
            "• All 3 modules: CRM, Task Management, Inventory/Finance\n"
            "• Up to 50 user seats\n"
            "• Priority support (chat + phone)\n"
            "• Custom fields &amp; workflow automation\n"
            "• Quarterly business-review session\n"
        ),
    ),
    "enterprise": PricingPlan(
        key="enterprise",
        name="🏢 Enterprise",
        price_label="Custom quote",
        summary_html=(
            "<b>🏢 Enterprise Plan</b>\n\n"
            "For large organizations with custom integration and compliance needs.\n\n"
            "<b>Includes:</b>\n"
            "• All modules + custom module development\n"
            "• Unlimited user seats\n"
            "• Dedicated account manager &amp; 24/7 support\n"
            "• On-premise or private-cloud deployment options\n"
            "• SLA-backed uptime guarantee\n"
        ),
    ),
}

PRICING_ORDER: list[str] = ["starter", "professional", "enterprise"]


# ---------------------------------------------------------------------------
# About Us
# ---------------------------------------------------------------------------

ABOUT_US_HTML = (
    "<b>🏢 About NovaERP Solutions</b>\n\n"
    "NovaERP Solutions builds all-in-one ERP software that helps small and "
    "mid-sized businesses run their sales, projects, and finances from a "
    "single platform.\n\n"
    "<b>🎯 Our Mission</b>\n"
    "Make enterprise-grade business software simple enough for any team to "
    "adopt in days, not months.\n\n"
    "<b>📈 By the numbers</b>\n"
    "• 1,200+ companies onboarded\n"
    "• 99.95% platform uptime (last 12 months)\n"
    "• Support in Persian and English\n\n"
    "<b>📍 Headquarters:</b> Tehran, Iran\n"
)


# ---------------------------------------------------------------------------
# Demo request flow copy
# ---------------------------------------------------------------------------

DEMO_INTRO_HTML = (
    "<b>🚀 Request a Live Demo</b>\n\n"
    "Tell us a little about your needs and our sales engineer will reach "
    "out to schedule a personalized walkthrough.\n\n"
    "Please reply with your <b>full name</b>, <b>company name</b>, and "
    "<b>phone number</b> in a single message, for example:\n"
    "<code>Jane Doe, Acme Co, +98 912 000 0000</code>\n\n"
    "Or just tap a button below to skip straight to contacting our sales team."
)

DEMO_THANKYOU_HTML = (
    "<b>✅ Thanks! Your demo request was received.</b>\n\n"
    "Our sales team will contact you within 1 business day.\n"
    "If it's urgent, you can also reach us directly — see the "
    "📞 <b>Contact / Support</b> button below."
)


# ---------------------------------------------------------------------------
# Contact / Support
# ---------------------------------------------------------------------------

def contact_html(company_name: str, phone: str, email: str, bale_username: str, website: str) -> str:
    return (
        f"<b>📞 Contact &amp; Support — {company_name}</b>\n\n"
        f"☎️ Phone: <code>{phone}</code>\n"
        f"✉️ Email: <code>{email}</code>\n"
        f"💬 Bale: {bale_username}\n"
        f"🌐 Website: {website}\n\n"
        "Our support team typically replies within a few hours on business days."
    )


# ---------------------------------------------------------------------------
# Main menu welcome text
# ---------------------------------------------------------------------------

WELCOME_HTML = (
    "<b>👋 Welcome to NovaERP Solutions!</b>\n\n"
    "I'm your virtual assistant. I can tell you about our ERP/CRM products, "
    "share pricing plans, or set up a live demo with our sales team.\n\n"
    "Use the menu below to get started 👇"
)

MAIN_MENU_PROMPT_HTML = "<b>🏠 Main Menu</b>\nWhat would you like to explore?"
