"""Register all bot routers."""

from __future__ import annotations

from aiogram import Router

from bot.handlers import callbacks, commands, reply_menu


def build_root_router() -> Router:
    root = Router(name="root")
    root.include_router(commands.router)
    root.include_router(reply_menu.router)
    root.include_router(callbacks.router)
    return root
