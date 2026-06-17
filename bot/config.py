"""Application configuration loaded from environment variables."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PACKAGE_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = PACKAGE_ROOT.parent
ASSETS_DIR = PROJECT_ROOT / "assets"


@dataclass(frozen=True, slots=True)
class Settings:
    """Runtime settings for the Bale bot."""

    bot_token: str
    api_base_url: str
    activity_db_path: Path
    activity_log_path: Path
    parse_mode: str = "HTML"

    @classmethod
    def from_env(cls) -> Settings:
        token = os.getenv("BALE_BOT_TOKEN", "").strip()
        if not token or token == "your_bot_token_here":
            raise ValueError(
                "BALE_BOT_TOKEN is missing. Copy .env.example to .env and set your token."
            )

        db_path = Path(os.getenv("ACTIVITY_DB_PATH", "data/user_activity.db"))
        log_path = Path(os.getenv("ACTIVITY_LOG_PATH", "user_activity.log"))

        if not db_path.is_absolute():
            db_path = PROJECT_ROOT / db_path
        if not log_path.is_absolute():
            log_path = PROJECT_ROOT / log_path

        return cls(
            bot_token=token,
            api_base_url=os.getenv("BALE_API_BASE_URL", "https://tapi.bale.ai").rstrip("/"),
            activity_db_path=db_path,
            activity_log_path=log_path,
        )


def create_bot_session(api_base_url: str):
    """Build an aiogram HTTP session pointed at Bale's Bot API."""
    from aiogram.client.session.aiohttp import AiohttpSession
    from aiogram.client.telegram import TelegramAPIServer

    session = AiohttpSession(api=TelegramAPIServer.from_base(api_base_url))
    return session
