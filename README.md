# Bale ERP Marketing Bot

Production-ready, **standalone** Python bot for [Bale Messenger](https://docs.bale.ai/) using **aiogram 3** with a configurable API base URL (`https://tapi.bale.ai`).

No external admin panel or APIs — all menus, copy, and routes are hardcoded.

## Features

- **Mixed keyboard UX**
  - Persistent **reply keyboard**: `🏠 Main Menu`, `📞 Contact / Support`
  - **Inline keyboards** for nested menus (products, pricing, about, demo)
- **Full navigation** with `🔙 Back` / `🏠 Main Menu` on every sub-screen
- **Local activity tracking** — SQLite (`data/user_activity.db`) + append-only `user_activity.log`
- **Rich HTML** messages; optional local **images** and **PDF brochures** per product

## Project structure

```
bale/
├── main.py                 # Entry point
├── requirements.txt
├── .env.example
├── assets/
│   ├── products/           # Optional PNG/JPG product images
│   └── brochures/          # Optional PDF feature lists
└── bot/
    ├── config.py           # Token, Bale API base URL, paths
    ├── callbacks.py        # Short callback_data tokens
    ├── content.py          # Hardcoded ERP/CRM copy
    ├── keyboards.py        # Reply + inline keyboard builders
    ├── navigation.py       # ROUTES dictionary & Screen model
    ├── activity_logger.py  # SQLite + text file logging
    ├── menu_state.py       # Per-chat menu message_id tracking
    ├── screen_renderer.py  # editMessage / sendPhoto / sendDocument
    ├── middlewares.py
    └── handlers/
        ├── commands.py     # /start, /help, /menu
        ├── reply_menu.py   # Bottom reply keyboard + free-text log
        └── callbacks.py    # Inline button routing
```

## Quick start

1. Create a bot via [Bale BotFather](https://ble.ir/botfather) and copy the token.

2. Install dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

3. Configure environment:

```bash
copy .env.example .env
# Edit .env and set BALE_BOT_TOKEN
```

4. Run:

```bash
python main.py
```

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `BALE_BOT_TOKEN` | — | Bot token from BotFather |
| `BALE_API_BASE_URL` | `https://tapi.bale.ai` | Bale Bot API base ([docs](https://docs.bale.ai/)) |
| `ACTIVITY_DB_PATH` | `data/user_activity.db` | SQLite path for behavior analytics |
| `ACTIVITY_LOG_PATH` | `user_activity.log` | Human-readable sequential log |

## Menu tree & routing

Callback tokens are defined in `bot/callbacks.py`. Screen content and keyboards are wired in `bot/navigation.py`:

| Callback | Screen |
|----------|--------|
| `nav:main` | Main menu |
| `nav:products` | Product list |
| `prod:crm` | CRM details |
| `prod:task` | Task & Project Management |
| `prod:inv` | Inventory/Finance |
| `nav:pricing` | Pricing plans |
| `nav:about` | About us |
| `nav:demo` | Request demo |
| `demo:{key}` | Demo request for a product |
| `nav:contact` | Contact / support |

Inline transitions use `editMessageText` when possible to keep the chat clean; product screens with images send `sendPhoto` (+ optional `sendDocument` for PDFs).

## Activity logging

Every interaction is logged with UTC timestamp, `user_id`, and exact payload:

- `command` — `/start`, `/help`, …
- `reply_keyboard` — bottom menu presses
- `inline_callback` — inline button `callback_data`
- `free_text` — user-typed messages (e.g. demo follow-up details)

**SQLite example** — user journey:

```sql
SELECT timestamp_utc, action_type, action_payload
FROM user_activity
WHERE user_id = 123456789
ORDER BY id;
```

**Text log** line format:

```
2026-06-17T10:15:30+00:00 | user_id=123 | type=inline_callback | payload='nav:products' | screen=nav:products
```

## Customization

- Edit copy in `bot/content.py`
- Add screens in `bot/navigation.py` and matching callbacks in `bot/callbacks.py`
- Add keyboard rows in `bot/keyboards.py`
- Drop images/PDFs under `assets/` (paths in `ProductContent`)

## Bale API note

Bale’s Bot API is Telegram-compatible. Requests go to:

`https://tapi.bale.ai/bot<token>/METHOD_NAME`

This project sets that via aiogram’s `TelegramAPIServer.from_base()` in `bot/config.py`.
