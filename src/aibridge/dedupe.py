"""In-process event dedupe store keyed by (channel, event_id)."""

from __future__ import annotations

import time
from collections.abc import Callable
from threading import Lock
from typing import Any, Literal


class EventDedupeStore:
    """Returns stored response bodies for duplicate events (no second side-effect)."""

    def __init__(self) -> None:
        self._lock = Lock()
        self._responses: dict[tuple[str, str], dict[str, Any]] = {}
        self._side_effect_counts: dict[tuple[str, str], int] = {}
        self._inflight: set[tuple[str, str]] = set()

    def get(self, channel: str, event_id: str) -> dict[str, Any] | None:
        with self._lock:
            stored = self._responses.get((channel, event_id))
            return None if stored is None else dict(stored)

    def try_begin(
        self, channel: str, event_id: str
    ) -> tuple[dict[str, Any] | None, Literal["hit", "begin", "inflight"]]:
        """Claim side-effect before engine (G-03). Loser must not call Responses."""
        key = (channel, event_id)
        with self._lock:
            existing = self._responses.get(key)
            if existing is not None:
                return dict(existing), "hit"
            if key in self._inflight:
                return None, "inflight"
            self._inflight.add(key)
            return None, "begin"

    def complete(self, channel: str, event_id: str, body: dict[str, Any]) -> None:
        key = (channel, event_id)
        with self._lock:
            self._responses[key] = dict(body)
            self._side_effect_counts[key] = self._side_effect_counts.get(key, 0) + 1
            self._inflight.discard(key)

    def abort(self, channel: str, event_id: str) -> None:
        key = (channel, event_id)
        with self._lock:
            self._inflight.discard(key)

    def wait_for_result(
        self,
        channel: str,
        event_id: str,
        *,
        timeout_s: float = 5.0,
        poll_s: float = 0.01,
    ) -> dict[str, Any] | None:
        """Poll until peer completes claim (or timeout)."""
        deadline = time.monotonic() + timeout_s
        while time.monotonic() < deadline:
            body = self.get(channel, event_id)
            if body is not None:
                return body
            with self._lock:
                if (channel, event_id) not in self._inflight:
                    return self.get(channel, event_id)
            time.sleep(poll_s)
        return self.get(channel, event_id)

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
            self._inflight.clear()
