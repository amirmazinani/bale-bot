"""
utils/logging_setup.py
=======================
Local, file + console logging. No external logging services (e.g. Sentry,
ELK) are wired up by default, per the "self-contained" requirement -- but
the structure here (a single configure_logging() call, module-level
loggers via logging.getLogger(__name__)) makes it trivial to add a handler
later without touching call sites.

Log files rotate daily-ish by size to avoid unbounded growth on a
long-running VM, which is a common real-world failure mode for "it works
in testing" bots.
"""

from __future__ import annotations

import logging
import logging.handlers
import sys
from pathlib import Path


def configure_logging(log_dir: Path, level: str = "INFO", log_to_file: bool = True) -> None:
    log_dir.mkdir(parents=True, exist_ok=True)

    root = logging.getLogger()
    root.setLevel(level.upper())

    fmt = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler -- always on, useful under systemd/docker logs.
    console_handler = logging.StreamHandler(stream=sys.stdout)
    console_handler.setFormatter(fmt)
    root.addHandler(console_handler)

    if log_to_file:
        file_handler = logging.handlers.RotatingFileHandler(
            filename=log_dir / "bot.log",
            maxBytes=5 * 1024 * 1024,   # 5 MB per file
            backupCount=5,              # keep last 5 rotations (~25 MB total)
            encoding="utf-8",
        )
        file_handler.setFormatter(fmt)
        root.addHandler(file_handler)

    # Quiet down noisy third-party loggers so our own INFO logs aren't
    # drowned out by aiohttp's connection-pool chatter.
    logging.getLogger("aiohttp.access").setLevel(logging.WARNING)
    logging.getLogger("aiogram.event").setLevel(logging.WARNING)
