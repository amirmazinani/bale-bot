"""In-memory per-chat menu message tracking for edit-based navigation."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class MenuStateStore:
    """Maps chat_id -> message_id of the current inline menu message."""

    _chat_menu_message: dict[int, int] = field(default_factory=dict)

    def set_menu_message(self, chat_id: int, message_id: int) -> None:
        self._chat_menu_message[chat_id] = message_id

    def get_menu_message(self, chat_id: int) -> int | None:
        return self._chat_menu_message.get(chat_id)

    def clear(self, chat_id: int) -> None:
        self._chat_menu_message.pop(chat_id, None)
