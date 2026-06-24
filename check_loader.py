#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

# Force reload content.loader
import importlib
import content.loader

# Reload module to pick up new JSON
importlib.reload(content.loader)

from content.loader import REPLY_KEYBOARD_BUTTONS, BTN_MAIN_MENU, BTN_CONTACT

print("Checking loader...")
print("-" * 40)

print("REPLY_KEYBOARD_BUTTONS:")
for i, btn in enumerate(REPLY_KEYBOARD_BUTTONS):
    print(f"  [{i}] text={btn['text']!r}, action={btn.get('action', 'N/A')}")

print()
print("BTN_MAIN_MENU =", repr(BTN_MAIN_MENU))
print("BTN_CONTACT =", repr(BTN_CONTACT))

print()
print("-" * 40)
print("Checking handler match:")
print("Expected text for main menu handler:", repr(BTN_MAIN_MENU))
print("Handler will match exactly this text.")

# Also check that reply_menu.py imports correctly
try:
    import handlers.reply_menu
    print("✓ reply_menu.py imports OK")
except Exception as e:
    print(f"✗ reply_menu.py import error: {e}")
