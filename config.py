"""
config.py
=========
Central configuration for the ERP/CRM Bale Bot.

All environment-dependent values (tokens, API base URL, file paths, log level)
live here so the rest of the codebase never hardcodes them. This is the ONLY
file you typically need to touch when deploying to a new bot account/environment.

Bale's Bot API is a Telegram-protocol-compatible HTTP API. The official base
endpoint is documented at https://docs.bale.ai and is reachable at:

    https://tapi.bale.ai/bot<TOKEN>/<method>

Because aiogram (and the underlying Telegram Bot API libraries) hardcode
"https://api.telegram.org/bot" as their default base URL, we override that
at the Session level (see bot_instance.py) using BALE_API_BASE_URL below.
This is what makes the "same code talks to Telegram OR Bale" trick work.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    # --- Core credentials -------------------------------------------------
    # NEVER hardcode the real token in source. Read from environment,
    # fall back to a placeholder so the script is still "runnable" for review.
    BOT_TOKEN: str = os.getenv("BALE_BOT_TOKEN", "PUT_YOUR_BALE_BOT_TOKEN_HERE")

    # --- API endpoint (the key Bale-vs-Telegram switch) --------------------
    # Bale's Telegram-compatible Bot API base URL (see docs.bale.ai).
    # Keeping this configurable means the exact same code can target a
    # Telegram bot for local testing simply by changing this env var to
    # "https://api.telegram.org/bot{token}/{method}".
    API_BASE_URL_TEMPLATE: str = os.getenv(
        "BOT_API_BASE_URL_TEMPLATE",
        "https://tapi.bale.ai/bot{token}/{method}",
    )
    API_FILE_URL_TEMPLATE: str = os.getenv(
        "BOT_API_FILE_URL_TEMPLATE",
        "https://tapi.bale.ai/file/bot{token}/{path}",
    )

    # --- Networking ----------------------------------------------------
    USE_WEBHOOK: bool = os.getenv("USE_WEBHOOK", "false").lower() == "true"
    WEBHOOK_HOST: str = os.getenv("WEBHOOK_HOST", "https://yourdomain.example.com")
    WEBHOOK_PATH: str = os.getenv("WEBHOOK_PATH", "/webhook/bale")
    WEBAPP_HOST: str = os.getenv("WEBAPP_HOST", "0.0.0.0")
    WEBAPP_PORT: int = int(os.getenv("WEBAPP_PORT", "8080"))

    # --- Business / support contact info (hardcoded ERP company info) -----
    COMPANY_NAME: str = "تراز سامانه"
    SUPPORT_PHONE: str = "+982191000000"
    SUPPORT_EMAIL: str = "support@tarazerp.example.com"
    SALES_BALE_USERNAME: str = "@tarazerp_sales"
    COMPANY_WEBSITE: str = "https://tarazerp.example.com"

    # --- Paths --------------------------------------------------------
    BASE_DIR: Path = field(default_factory=lambda: Path(__file__).resolve().parent)
    ASSETS_DIR: Path = field(default_factory=lambda: Path(__file__).resolve().parent / "assets")
    LOG_DIR: Path = field(default_factory=lambda: Path(__file__).resolve().parent / "logs")

    # --- Logging --------------------------------------------------------
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_TO_FILE: bool = os.getenv("LOG_TO_FILE", "true").lower() == "true"

    # --- Misc behavior ----------------------------------------------------
    DEMO_REQUEST_NOTIFY_ADMIN_CHAT_ID: int | None = (
        int(os.getenv("ADMIN_CHAT_ID")) if os.getenv("ADMIN_CHAT_ID") else None
    )


settings = Settings()