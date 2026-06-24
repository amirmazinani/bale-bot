#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import json

# First check raw JSON
with open('content/content.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    
print("Raw JSON reply_keyboard buttons:")
for btn in data['reply_keyboard']['buttons']:
    print(f"  text: {btn['text']!r}")
    print(f"  action: {btn.get('action', 'N/A')}")
    print()

# Now load from module
import importlib
import content.loader
importlib.reload(content.loader)

print("From content.loader.REPLY_KEYBOARD_BUTTONS:")
for btn in content.loader.REPLY_KEYBOARD_BUTTONS:
    print(f"  text: {btn['text']!r}")
    print(f"  action: {btn.get('action', 'N/A')}")
    print()

# Check reply.py constants
import keyboards.reply
print(f"keyboards.reply.BTN_MAIN_MENU = {keyboards.reply.BTN_MAIN_MENU!r}")
print(f"keyboards.reply.BTN_CONTACT = {keyboards.reply.BTN_CONTACT!r}")
print()

# Test matching
test_messages = [
    "🏠 منوی اصلی",
    "📞 تماس / پشتیبانی",
    "🏠 Main Menu",  # old
    "📞 Contact / Support",  # old
]

print("Testing text matching:")
for msg in test_messages:
    main_match = msg == keyboards.reply.BTN_MAIN_MENU
    contact_match = msg == keyboards.reply.BTN_CONTACT
    print(f"  {msg!r}: main_menu={main_match}, contact={contact_match}")
