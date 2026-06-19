"""
utils/fsm.py
============
A deliberately tiny, dependency-free in-memory state store.

The only place this bot needs "memory" of what the user is doing is the
single free-text step of the demo-request flow ("please type your name,
company, phone"). Everything else is pure stateless navigation (see
utils/navigation.py), so we don't need aiogram's full FSMContext/Storage
machinery -- a plain dict keyed by chat_id is sufficient, transparent, and
has zero external dependencies (no Redis, no DB), matching the
"self-contained, no external services" requirement.

If you outgrow this (e.g. need persistence across restarts), swap this
module's internals for aiogram's RedisStorage/SQLite storage without
touching any handler code, since handlers only call the functions below.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field

# State machine "modes" a chat can be in.
MODE_IDLE = "idle"
MODE_AWAITING_DEMO_INFO = "awaiting_demo_info"


@dataclass
class ChatState:
    mode: str = MODE_IDLE
    # product_key is set when the user requested a demo *for a specific
    # product* (vs. the generic "Request a Demo" main-menu entry point).
    product_key: str | None = None
    updated_at: float = field(default_factory=time.time)


class FSMStore:
    """Process-local store: {chat_id: ChatState}."""

    def __init__(self) -> None:
        self._states: dict[int, ChatState] = {}

    def get(self, chat_id: int) -> ChatState:
        return self._states.setdefault(chat_id, ChatState())

    def set_awaiting_demo_info(self, chat_id: int, product_key: str | None = None) -> None:
        self._states[chat_id] = ChatState(
            mode=MODE_AWAITING_DEMO_INFO,
            product_key=product_key,
            updated_at=time.time(),
        )

    def reset(self, chat_id: int) -> None:
        self._states[chat_id] = ChatState()

    def is_awaiting_demo_info(self, chat_id: int) -> bool:
        return self.get(chat_id).mode == MODE_AWAITING_DEMO_INFO


# Module-level singleton -- imported by handlers. For a multi-process
# deployment behind a load balancer you'd back this with Redis instead;
# for a single-process polling/webhook bot (the common case for this kind
# of self-contained ERP bot) this is sufficient and simple.
fsm_store = FSMStore()
