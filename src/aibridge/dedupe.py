"""In-process event dedupe store keyed by (channel, event_id)."""

from __future__ import annotations

from collections.abc import Callable
from threading import Lock
from typing import Any


class EventDedupeStore:
    """Returns stored response bodies for duplicate events (no second side-effect)."""

    def __init__(self) -> None:
        self._lock = Lock()
        self._responses: dict[tuple[str, str], dict[str, Any]] = {}
        self._side_effect_counts: dict[tuple[str, str], int] = {}

    def get(self, channel: str, event_id: str) -> dict[str, Any] | None:
        with self._lock:
            stored = self._responses.get((channel, event_id))
            return None if stored is None else dict(stored)

    def get_or_create(
        self,
        channel: str,
        event_id: str,
        factory: Callable[[], dict[str, Any]],
    ) -> tuple[dict[str, Any], bool]:
        """Return stored response or create via factory once under lock."""
        key = (channel, event_id)
        with self._lock:
            existing = self._responses.get(key)
            if existing is not None:
                return dict(existing), False
            body = dict(factory())
            self._responses[key] = body
            self._side_effect_counts[key] = self._side_effect_counts.get(key, 0) + 1
            return dict(body), True

    def side_effect_count(self, channel: str, event_id: str) -> int:
        with self._lock:
            return self._side_effect_counts.get((channel, event_id), 0)

    def clear(self) -> None:
        with self._lock:
            self._responses.clear()
            self._side_effect_counts.clear()
