"""Redacted audit logging — AIB-SEC-02 (story 06)."""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from typing import Any

# Patterns that must never appear in audit/default log records.
_SECRET_PATTERNS = (
    re.compile(r"(?i)bearer\s+[a-z0-9._\-]+"),
    re.compile(r"(?i)(api[_-]?key|token)\s*[:=]\s*\S+"),
)

_logger = logging.getLogger("aibridge.audit")


@dataclass
class AuditBuffer:
    """In-memory capture for tests — never stores raw narrative bodies."""

    records: list[dict[str, Any]] = field(default_factory=list)

    def clear(self) -> None:
        self.records.clear()

    def dump_text(self) -> str:
        parts: list[str] = []
        for rec in self.records:
            parts.append(str(rec.get("event", "")))
            parts.append(str(rec.get("detail", "")))
        return "\n".join(parts)


_buffer = AuditBuffer()


def get_audit_buffer() -> AuditBuffer:
    return _buffer


def reset_audit_buffer() -> AuditBuffer:
    _buffer.clear()
    return _buffer


def redact_text(value: str) -> str:
    """Strip bearer/token shapes; truncate long free text."""
    out = value
    for pat in _SECRET_PATTERNS:
        out = pat.sub("[REDACTED]", out)
    if len(out) > 120:
        out = out[:117] + "..."
    return out


def audit_event(
    event: str,
    *,
    detail: str = "",
    include_narrative: bool = False,
) -> None:
    """Emit structured audit metadata.

    ``include_narrative`` is always forced False for default path — narrative
    bodies are never logged (privacy-pilot).
    """
    _ = include_narrative  # API clarity; narrative never recorded.
    safe_detail = redact_text(detail) if detail else ""
    # Drop anything that looks like a long resident message.
    if len(safe_detail) > 80:
        safe_detail = f"len={len(detail)}"
    rec = {"event": event, "detail": safe_detail}
    _buffer.records.append(rec)
    _logger.info("audit event=%s detail=%s", event, safe_detail or "-")


def assert_phrase_absent(haystack: str, phrase: str) -> None:
    if phrase and phrase in haystack:
        raise AssertionError("privacy test phrase leaked into logs/metrics")
