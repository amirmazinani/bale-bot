"""Hardcoded ERP/CRM copy, assets, and company information."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from bot.config import ASSETS_DIR

COMPANY_NAME = "NovaERP Solutions"
COMPANY_TAGLINE = "Integrated CRM, Projects & Finance for growing businesses"


@dataclass(frozen=True, slots=True)
class ProductContent:
    key: str
    title: str
    short_label: str
    description_html: str
    image_path: Path | None
    brochure_pdf_path: Path | None


WELCOME_HTML = f"""
<b>Welcome to {COMPANY_NAME}</b> 🚀

{COMPANY_TAGLINE}

Use the <b>bottom menu</b> for quick access, or choose an option below to explore our platform.
""".strip()

MAIN_MENU_HTML = f"""
<b>🏠 Main Menu</b>

Select what you would like to explore:

• <b>Our Products</b> — CRM, Tasks, Inventory & Finance
• <b>Pricing Plans</b> — transparent tiers for every team size
• <b>About Us</b> — who we are and how we help
• <b>Request a Demo</b> — book a live walkthrough
""".strip()

PRODUCTS_MENU_HTML = """
<b>📦 Our Products</b>

Choose a product to view features and capabilities:
""".strip()

PRICING_HTML = """
<b>💰 Pricing Plans</b>

<b>Starter</b> — $29/user/month
• Up to 10 users
• CRM + Task Management
• Email support

<b>Professional</b> — $59/user/month
• Unlimited users
• Full CRM, Projects & Inventory
• Priority support + onboarding

<b>Enterprise</b> — Custom pricing
• Dedicated account manager
• SSO, custom integrations & SLA
• On-premise deployment option

<i>All plans include a 14-day free trial. Annual billing saves 20%.</i>
""".strip()

ABOUT_HTML = f"""
<b>🏢 About {COMPANY_NAME}</b>

We build <b>all-in-one ERP software</b> for SMEs and mid-market companies across the Middle East and beyond.

<b>What we deliver:</b>
• Customer Relationship Management (CRM)
• Task & Project Management
• Inventory, invoicing & financial reporting
• Unified dashboards and role-based access

<b>Why teams choose us:</b>
✅ Fast deployment (days, not months)
✅ Persian/English bilingual UI
✅ Local support & training
✅ No external admin panel required for day-to-day ops

<i>Founded 2018 · 200+ active clients · ISO-aligned processes</i>
""".strip()

DEMO_HTML = """
<b>🚀 Request a Demo</b>

Thank you for your interest! Our sales team will contact you within <b>1 business day</b>.

<b>To speed things up, please reply with:</b>
1. Company name
2. Team size
3. Products you are interested in
4. Preferred contact method (phone / email)

Or reach us directly:
📞 <b>+98 21 1234 5678</b>
📧 <b>sales@novaerp.example</b>
""".strip()

CONTACT_HTML = """
<b>📞 Contact & Support</b>

<b>Sales:</b> sales@novaerp.example · +98 21 1234 5678
<b>Support:</b> support@novaerp.example · +98 21 1234 5679

<b>Working hours:</b> Sat–Thu, 9:00–18:00 (Tehran)

<b>Office:</b>
Tehran, Valiasr St., Innovation Tower, Floor 12

We typically respond within <b>2 hours</b> during business hours.
""".strip()

PRODUCTS: dict[str, ProductContent] = {
    "crm": ProductContent(
        key="crm",
        title="Customer Relationship Management (CRM)",
        short_label="Customer Relationship Management (CRM)",
        description_html="""
<b>📊 Customer Relationship Management (CRM)</b>

Centralize leads, accounts, and pipelines in one workspace.

<b>Key features:</b>
• Lead capture & scoring
• 360° customer profiles
• Sales pipeline & forecasting
• Activity timeline (calls, meetings, notes)
• Email templates & follow-up reminders
• Role-based dashboards for reps and managers

<b>Ideal for:</b> sales teams, account managers, and customer success.

<i>Replace spreadsheets with a single source of truth for every customer touchpoint.</i>
""".strip(),
        image_path=ASSETS_DIR / "products" / "crm_overview.png",
        brochure_pdf_path=ASSETS_DIR / "brochures" / "crm_features.pdf",
    ),
    "task": ProductContent(
        key="task",
        title="Task & Project Management",
        short_label="Task & Project Management",
        description_html="""
<b>✅ Task & Project Management</b>

Plan, assign, and deliver work with full visibility.

<b>Key features:</b>
• Projects, boards & Kanban views
• Task dependencies & milestones
• Time tracking & workload view
• File attachments per task
• Team comments & @mentions
• Gantt charts & burndown reports

<b>Ideal for:</b> operations, engineering, marketing, and PMO teams.

<i>Keep deadlines visible and accountability clear across departments.</i>
""".strip(),
        image_path=ASSETS_DIR / "products" / "task_overview.png",
        brochure_pdf_path=ASSETS_DIR / "brochures" / "task_features.pdf",
    ),
    "inv": ProductContent(
        key="inv",
        title="Inventory / Finance System",
        short_label="Inventory/Finance System",
        description_html="""
<b>📦 Inventory & Finance System</b>

Control stock, purchases, invoicing, and cash flow.

<b>Key features:</b>
• Multi-warehouse inventory
• Purchase orders & supplier management
• Sales invoices & payment tracking
• Tax-ready financial reports
• Low-stock alerts & reorder rules
• Export to Excel / PDF

<b>Ideal for:</b> finance, warehouse, and procurement teams.

<i>Connect sales and operations with real-time stock and revenue data.</i>
""".strip(),
        image_path=ASSETS_DIR / "products" / "inventory_overview.png",
        brochure_pdf_path=ASSETS_DIR / "brochures" / "inventory_features.pdf",
    ),
}

PRODUCT_CALLBACK_TO_KEY: dict[str, str] = {
    "prod:crm": "crm",
    "prod:task": "task",
    "prod:inv": "inv",
}
