"""Chronological user interaction logging (SQLite + plain-text file)."""

from __future__ import annotations

import asyncio
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class ActivityLogger:
    """Thread-safe async wrapper around SQLite and append-only text log."""

    def __init__(self, db_path: Path, log_path: Path) -> None:
        self._db_path = db_path
        self._log_path = log_path
        self._lock = asyncio.Lock()

    async def setup(self) -> None:
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        self._log_path.parent.mkdir(parents=True, exist_ok=True)
        await asyncio.to_thread(self._init_db)

    def _init_db(self) -> None:
        with sqlite3.connect(self._db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS user_activity (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp_utc TEXT NOT NULL,
                    user_id INTEGER NOT NULL,
                    username TEXT,
                    full_name TEXT,
                    action_type TEXT NOT NULL,
                    action_payload TEXT NOT NULL,
                    screen_id TEXT
                )
                """
            )
            conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_user_activity_user_time
                ON user_activity (user_id, timestamp_utc)
                """
            )
            conn.commit()

    async def log(
        self,
        *,
        user_id: int,
        username: str | None,
        full_name: str | None,
        action_type: str,
        action_payload: str,
        screen_id: str | None = None,
    ) -> None:
        timestamp = datetime.now(timezone.utc).isoformat()
        record = {
            "timestamp_utc": timestamp,
            "user_id": user_id,
            "username": username,
            "full_name": full_name,
            "action_type": action_type,
            "action_payload": action_payload,
            "screen_id": screen_id,
        }
        async with self._lock:
            await asyncio.to_thread(self._write_record, record)

    def _write_record(self, record: dict[str, Any]) -> None:
        with sqlite3.connect(self._db_path) as conn:
            conn.execute(
                """
                INSERT INTO user_activity (
                    timestamp_utc, user_id, username, full_name,
                    action_type, action_payload, screen_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    record["timestamp_utc"],
                    record["user_id"],
                    record["username"],
                    record["full_name"],
                    record["action_type"],
                    record["action_payload"],
                    record["screen_id"],
                ),
            )
            conn.commit()

        line = (
            f"{record['timestamp_utc']} | user_id={record['user_id']} | "
            f"type={record['action_type']} | payload={record['action_payload']!r}"
        )
        if record["screen_id"]:
            line += f" | screen={record['screen_id']}"
        if record["username"]:
            line += f" | username=@{record['username']}"
        line += "\n"
        with self._log_path.open("a", encoding="utf-8") as log_file:
            log_file.write(line)
