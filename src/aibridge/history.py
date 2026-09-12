"""Replayable Responses conversation history (local; bundle-pinned session)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class HistoryStore:
    """In-process history keyed by session_id (Postgres persistence can wrap later)."""

    _items: dict[str, list[dict[str, Any]]] = field(default_factory=dict)

    def append(self, session_id: str, item: dict[str, Any]) -> None:
        self._items.setdefault(session_id, []).append(dict(item))

    def list_items(self, session_id: str) -> list[dict[str, Any]]:
        return [dict(x) for x in self._items.get(session_id, [])]

    def replace(self, session_id: str, items: list[dict[str, Any]]) -> None:
        self._items[session_id] = [dict(x) for x in items]

    def clear(self, session_id: str) -> None:
        self._items.pop(session_id, None)
