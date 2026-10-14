"""PII-safe observability for bind jobs (REQ-09 §4.6)."""

from __future__ import annotations

import logging
import time

from aibridge.audit import audit_event

_logger = logging.getLogger("aibridge.sense_bind")


def log_bind_job(
    *,
    issue_id: str,
    generation_version: str,
    event: str,
    success: bool | None = None,
    reason_class: str | None = None,
    latency_ms: float | None = None,
) -> None:
    """Log correlation ids / class / latency — never bodies, tokens, secrets."""
    parts = [f"issue_id={issue_id}", f"generation_version={generation_version}"]
    if success is not None:
        parts.append(f"success={success}")
    if reason_class:
        parts.append(f"reason_class={reason_class}")
    if latency_ms is not None:
        parts.append(f"latency_ms={latency_ms:.1f}")
    detail = " ".join(parts)
    _logger.info("sense_bind.%s %s", event, detail)
    audit_event(f"sense_bind.{event}", detail=detail)


class BindLatencyTimer:
    """Simple wall-clock timer for bind latency (no metric-backend SSOT)."""

    def __init__(self) -> None:
        self._t0 = time.perf_counter()

    def elapsed_ms(self) -> float:
        return (time.perf_counter() - self._t0) * 1000.0
