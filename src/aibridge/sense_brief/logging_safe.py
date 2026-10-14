"""PII-safe logging for sense-brief jobs — ids OK; bodies/secrets out."""

from __future__ import annotations

import logging

from aibridge.audit import audit_event

_logger = logging.getLogger("aibridge.sense_brief")


def log_brief_job(
    *,
    issue_id: str,
    generation_version: str,
    event: str,
    failure_class: str | None = None,
) -> None:
    """Log job identifiers only — never corpus text or citizen bodies."""
    parts = [f"issue_id={issue_id}", f"generation_version={generation_version}"]
    if failure_class:
        parts.append(f"failure_class={failure_class}")
    detail = " ".join(parts)
    _logger.info("sense_brief.%s %s", event, detail)
    audit_event(f"sense_brief.{event}", detail=detail)
