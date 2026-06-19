"""
handlers/demo_capture.py
==========================
Captures the single free-text message the user sends after tapping
"🚀 Request a Demo" / "🚀 Request Demo for this Product" -- i.e. their
name/company/phone line.

This is the one place in the bot that deals with plain-text input rather
than button taps, so it's deliberately isolated from menu_router.py. The
Router-level filter `fsm_store.is_awaiting_demo_info(...)` ensures this
handler ONLY fires when the user is actually in that flow; otherwise their
text falls through to handlers/fallback.py.

No external CRM/API call is made (per the "no external APIs" requirement).
Instead we:
  1. Log the lead locally (utils/logging_setup.py-configured logger), so
     ops can grep bot.log for "DEMO_LEAD" to find every request.
  2. Optionally forward it to an admin's chat_id if configured, using the
     SAME bot/session -- i.e. still 100% within Bale's API, no 3rd party.
"""

from __future__ import annotations

import logging

from aiogram import Bot, F, Router
from aiogram.types import Message

from config import settings
from content.erp_content import DEMO_THANKYOU_HTML, PRODUCTS
from keyboards.inline import demo_thankyou_keyboard
from utils.fsm import fsm_store

logger = logging.getLogger(__name__)
router = Router(name="demo_capture")


def _is_awaiting_demo_info(message: Message) -> bool:
    return fsm_store.is_awaiting_demo_info(message.chat.id)


@router.message(F.text, _is_awaiting_demo_info)
async def on_demo_info_provided(message: Message, bot: Bot) -> None:
    chat_state = fsm_store.get(message.chat.id)
    product_label = "General inquiry"
    if chat_state.product_key and chat_state.product_key in PRODUCTS:
        product_label = PRODUCTS[chat_state.product_key].title

    lead_text = message.text.strip()
    user = message.from_user

    # 1) Local structured log entry -- this is the bot's "CRM ingestion"
    #    in the absence of an external CRM API, per the self-contained
    #    requirement. Ops can tail/grep this safely.
    logger.info(
        "DEMO_LEAD | user_id=%s | username=%s | product=%s | raw_text=%r",
        user.id if user else "unknown",
        (user.username if user and user.username else "n/a"),
        product_label,
        lead_text,
    )

    # 2) Optional: forward to an admin chat using the SAME bot/session,
    #    so this stays "self-contained" (no external CRM/webhook call).
    if settings.DEMO_REQUEST_NOTIFY_ADMIN_CHAT_ID:
        try:
            await bot.send_message(
                chat_id=settings.DEMO_REQUEST_NOTIFY_ADMIN_CHAT_ID,
                text=(
                    f"<b>🆕 New Demo Request</b>\n"
                    f"Product: {product_label}\n"
                    f"From: {user.full_name if user else 'Unknown'} "
                    f"(@{user.username if user and user.username else 'n/a'}, id={user.id if user else 'n/a'})\n\n"
                    f"<b>Message:</b>\n{lead_text}"
                ),
                parse_mode="HTML",
            )
        except Exception:
            logger.exception("Failed to forward demo lead to admin chat.")

    fsm_store.reset(message.chat.id)
    await message.answer(DEMO_THANKYOU_HTML, reply_markup=demo_thankyou_keyboard(), parse_mode="HTML")
