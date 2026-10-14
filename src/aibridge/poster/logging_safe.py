"""PII-safe logging for poster/storage jobs — ids OK; bodies/secrets out."""

from __future__ import annotations

import logging

from aibridge.audit import audit_event

_logger = logging.getLogger("aibridge.poster")


def log_poster_job(
    *,
    issue_id: str,
    generation_version: str,
    event: str,
    failure_class: str | None = None,
) -> None:
    parts = [f"issue_id={issue_id}", f"generation_version={generation_version}"]
    if failure_class:
        parts.append(f"failure_class={failure_class}")
    detail = " ".join(parts)
    _logger.info("poster.%s %s", event, detail)
    audit_event(f"poster.{event}", detail=detail)
