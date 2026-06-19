# NovaERP Bale Bot

A self-contained, production-ready Bale messenger bot for an ERP/CRM software
company. Built on **aiogram 3.x**, pointed at **Bale's** Bot API
(`https://tapi.bale.ai/bot...`) instead of Telegram's, via one configurable
URL override — everything else is standard aiogram.

No external admin panel, no external CRM/API calls, no database. All menus,
copy, and pricing are hardcoded in `content/erp_content.py`.

## Quick start

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then edit .env with your real BALE_BOT_TOKEN
export $(grep -v '^#' .env | xargs)   # or use a process manager / docker env
python bot.py
```

By default the bot runs in **long-polling** mode, which needs no public
domain/SSL and is the simplest way to get started. Set `USE_WEBHOOK=true`
(plus `WEBHOOK_HOST`) to switch to webhook mode for production.

## How the Bale/Telegram switch works

aiogram builds every API request URL from a `TelegramAPIServer` template.
`bot_instance.py` swaps in Bale's templates:

```python
TelegramAPIServer(
    base="https://tapi.bale.ai/bot{token}/{method}",
    file="https://tapi.bale.ai/file/bot{token}/{path}",
)
```

Change `BOT_API_BASE_URL_TEMPLATE` / `BOT_API_FILE_URL_TEMPLATE` in `.env` to
Telegram's own URLs to run the exact same codebase against a real Telegram
bot for local testing — nothing else in the project needs to change.

## Project layout

```
erp_bale_bot/
├── bot.py                  # entrypoint: dispatcher assembly, polling/webhook
├── bot_instance.py          # Bot construction w/ Bale API base-URL override
├── config.py                 # all env-driven settings (tokens, URLs, paths)
├── requirements.txt
├── .env.example
├── content/
│   └── erp_content.py        # ALL hardcoded copy: products, pricing, about, demo text
├── keyboards/
│   ├── reply.py               # persistent bottom Reply Keyboard (2 buttons)
│   └── inline.py               # every inline keyboard, one factory per screen
├── handlers/
│   ├── start.py                 # /start
│   ├── reply_menu.py             # the 2 persistent reply-keyboard buttons
│   ├── menu_router.py             # single CallbackQuery entrypoint + dispatch table
│   ├── demo_capture.py             # captures the free-text demo-request reply
│   └── fallback.py                  # catch-all for unrecognized text
├── utils/
│   ├── navigation.py                # route constants, parent-route graph, callback codec
│   ├── fsm.py                        # tiny in-memory per-chat state (demo flow only)
│   ├── screen.py                       # edit-in-place rendering helpers
│   └── logging_setup.py                 # rotating file + console logging
└── assets/                                # drop promo images / PDFs here (see assets/README.md)
```

## Navigation architecture

Every inline button carries a `callback_data` string like `menu:products` or
`menu:product_detail:crm`. `utils/navigation.py` defines:

- **Route constants** (`ROUTE_MAIN_MENU`, `ROUTE_PRODUCTS_LIST`, …)
- **`PARENT_ROUTES`**: a route → parent-route dict, i.e. the whole menu tree
  as data. This is what every "🔙 Back" button is derived from, so adding a
  new screen never requires manually re-wiring back-navigation elsewhere.
- **`CallbackData.encode()/decode()`**: turns a `(route, arg)` pair into a
  wire string and back, handling parameterized routes (e.g. which product).

`handlers/menu_router.py` has exactly **one** `@router.callback_query()`
handler. It decodes the tapped button's route, looks it up in the
`ROUTE_HANDLERS` dispatch dict, and calls the matching renderer function.
Unknown/stale routes fall back to the main menu rather than doing nothing —
the user can never get permanently stuck on a dead screen.

### Menu tree (as implemented)

```
🏠 Main Menu
├── 📦 Our Products
│   ├── Customer Relationship Management (CRM)
│   │     └── 🚀 Request Demo for this Product → demo capture (back → CRM page)
│   ├── Task & Project Management
│   │     └── 🚀 Request Demo for this Product
│   └── Inventory/Finance System
│         └── 🚀 Request Demo for this Product
├── 💰 Pricing Plans
│   ├── Starter
│   ├── Professional
│   └── Enterprise
├── 🏢 About Us
└── 🚀 Request a Demo (general) → demo capture (back → Main Menu)
```

Plus, always visible at the bottom: **🏠 Main Menu** and
**📞 Contact / Support** (Reply Keyboard, never goes away).

## Edit-in-place UX

`utils/screen.py::render_screen()` calls `message.edit_text(...)` on the
tapped message instead of sending a new one, so navigating through Products
→ CRM → Back → Pricing → Starter etc. edits a single message in place and
keeps the chat clean. If an edit fails (e.g. the original message was a
photo), it safely falls back to sending a new message instead of crashing
or leaving a stale screen.

## Rich content hooks (images / PDFs)

`content/erp_content.py`'s `Product` dataclass has `image_path` /
`pdf_path` fields. `handlers/menu_router.py::_render_product_detail`
already checks for the promo image on disk and sends it via
`answer_photo()` right before the text detail card — drop a real PNG at the
path in `assets/` and it activates automatically, no code changes. See
`assets/README.md` for exact filenames and how to wire up the PDF
feature-list button (left as a documented extension point).

## Demo-request flow & local "CRM" logging

Tapping "Request a Demo" puts that chat into an `awaiting_demo_info` state
(`utils/fsm.py` — a plain in-memory dict, no Redis/DB needed for this scope).
The next free-text message the user sends is captured by
`handlers/demo_capture.py`, which:

1. Logs a structured `DEMO_LEAD | ...` line via the standard logging module
   (`utils/logging_setup.py` → rotating file at `logs/bot.log`, 5 MB × 5
   backups). This is the bot's local lead-capture mechanism in place of an
   external CRM API.
2. Optionally forwards the lead to an admin's chat via `ADMIN_CHAT_ID`,
   using the *same* Bale bot session — still fully self-contained, no
   third-party HTTP calls.
3. Resets the chat's FSM state and shows a thank-you screen.

Tapping the persistent **🏠 Main Menu** button at any time also resets this
state, so a user can never get stuck mid-flow.

## Extending the menu

To add a new top-level menu item:

1. Add a `ROUTE_*` constant + its parent in `utils/navigation.py`.
2. Add a button referencing it in the relevant `keyboards/inline.py` factory.
3. Write a `_render_*` function in `handlers/menu_router.py` and register it
   in `ROUTE_HANDLERS`.

That's the entire contract — no other file needs to change.
