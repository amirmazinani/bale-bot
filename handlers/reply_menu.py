"""
handlers/reply_menu.py
=======================
Handlers for the two persistent Reply Keyboard buttons:
    🏠 Main Menu
    📞 Contact / Support

These match on literal message text (that's how Telegram/Bale reply
keyboards work -- tapping a button just sends its label as a normal text
message). Because they always send a NEW message (there's nothing to edit;
a reply-keyboard tap isn't a CallbackQuery), every other inline-menu screen
opened from here starts a fresh "edit chain" that subsequent inline taps
will edit in place.
"""

from __future__ import annotations

import logging

from aiogram import F, Router
from aiogram.types import Message

from content.loader import SCREENS
from keyboards.reply import REPLY_BUTTON_TEXTS
from utils.dynamic_navigation import get_route_for_screen
from utils.fsm import fsm_store
from utils.screen import send_screen

logger = logging.getLogger(__name__)
router = Router(name="reply_menu")


# Dynamic handler for all reply keyboard buttons
@router.message(F.text.in_(REPLY_BUTTON_TEXTS))
async def on_reply_button(message: Message) -> None:
    """Handle any reply keyboard button tap dynamically."""
    logger.info("user_id=%s tapped reply button (text=%r)", message.from_user.id, message.text)
    
    # Find the button from REPLY_KEYBOARD_BUTTONS
    from content.loader import REPLY_KEYBOARD_BUTTONS
    
    for button in REPLY_KEYBOARD_BUTTONS:
        if button["text"] == message.text:
            action = button.get("action")
            route_key = button.get("route")
            
            # Handle action-based buttons
            if action == "main_menu":
                fsm_store.reset(message.chat.id)
                s = SCREENS["main_menu"]
                await send_screen(message, s.text, s.keyboard)
                return
            elif action == "contact":
                s = SCREENS["contact"]
                await send_screen(message, s.text, s.keyboard)
                return
            
            # Handle route-based buttons dynamically
            elif route_key:
                # Get the screen if it exists
                if route_key in SCREENS:
                    s = SCREENS[route_key]
                    await send_screen(message, s.text, s.keyboard)
                    return
                else:
                    logger.warning("Route key %r not found in SCREENS", route_key)
            
            # Handle unknown actions
            else:
                logger.warning("Unknown action=%r for reply button text=%r", 
                             action, message.text)
                
    # If no matching button found, show main menu
    fsm_store.reset(message.chat.id)
    s = SCREENS["main_menu"]
    await send_screen(message, s.text, s.keyboard)
