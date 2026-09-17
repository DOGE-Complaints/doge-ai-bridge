"""In-process rate limits — enforce when Settings knobs are set (REQ-03 §5.6)."""

from __future__ import annotations

import hashlib
import time
from collections import defaultdict, deque
from dataclasses import dataclass, field


def hash_principal_key(authorization: str | None) -> str:
    """Opaque principal id — never store raw Authorization / Bearer prefix."""
    if not authorization:
        return "anonymous"
    digest = hashlib.sha256(authorization.encode("utf-8")).hexdigest()
    return f"p:{digest}"


@dataclass
class RateLimiter:
    """Sliding-window counters. Limits None → disabled."""

    principal_limit: int | None = None
    global_limit: int | None = None
    window_seconds: float = 60.0
    _principal: dict[str, deque[float]] = field(default_factory=lambda: defaultdict(deque))
    _global: deque[float] = field(default_factory=deque)

    def enabled(self) -> bool:
        return self.principal_limit is not None or self.global_limit is not None

    def _prune(self, q: deque[float], now: float) -> None:
        cutoff = now - self.window_seconds
        while q and q[0] < cutoff:
            q.popleft()

    def allow(self, principal_key: str, *, now: float | None = None) -> str | None:
        """Return None if allowed, else coarse reason code for 429."""
        if not self.enabled():
            return None
        ts = time.monotonic() if now is None else now
        if self.global_limit is not None:
            self._prune(self._global, ts)
            if len(self._global) >= self.global_limit:
                return "global_rate_limit"
        if self.principal_limit is not None:
            pq = self._principal[principal_key]
            self._prune(pq, ts)
            if len(pq) >= self.principal_limit:
                return "principal_rate_limit"
        if self.global_limit is not None:
            self._global.append(ts)
        if self.principal_limit is not None:
            self._principal[principal_key].append(ts)
        return None
