"""Per-session turn serialization (AIB-RSP-02)."""

from __future__ import annotations

import threading
from contextlib import contextmanager
from typing import Iterator


class SessionTurnLock:
    """At most one active Responses turn per session (in-process equivalent)."""

    def __init__(self) -> None:
        self._guard = threading.Lock()
        self._locks: dict[str, threading.Lock] = {}
        self._active: set[str] = set()

    def _lock_for(self, session_id: str) -> threading.Lock:
        with self._guard:
            if session_id not in self._locks:
                self._locks[session_id] = threading.Lock()
            return self._locks[session_id]

    @contextmanager
    def hold(self, session_id: str) -> Iterator[None]:
        lock = self._lock_for(session_id)
        if not lock.acquire(blocking=True):
            raise RuntimeError(f"failed to acquire turn lock: {session_id}")
        try:
            with self._guard:
                if session_id in self._active:
                    raise RuntimeError(f"turn already active: {session_id}")
                self._active.add(session_id)
            yield
        finally:
            with self._guard:
                self._active.discard(session_id)
            lock.release()

    def is_active(self, session_id: str) -> bool:
        with self._guard:
            return session_id in self._active
