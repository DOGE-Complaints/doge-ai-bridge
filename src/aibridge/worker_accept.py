"""Sense-brief worker accept — entry/auth/idempotency (STORY-AIBRIDGE-46).

Implement names (Open in arch; chosen for this wave, documented in task READMEs):
- Path: ``POST /v1/worker/sense-brief/accept``
- Prefix: ``/v1/worker/``
- Env: ``AIBRIDGE_WORKER_SENSE_BRIEF_ENABLED``, ``AIBRIDGE_WORKER_SENSE_BRIEF_S2S_TOKEN``
- JSON: ``issue_id``, ``generation_version``, optional ``corpus`` (opaque)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from threading import Lock
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


WORKER_PATH_PREFIX = "/v1/worker/"
WORKER_ACCEPT_PATH = "/v1/worker/sense-brief/accept"


class WorkerAcceptRequest(BaseModel):
    """Logical accept body — field names are implement choice (Open in arch)."""

    model_config = ConfigDict(extra="ignore")

    issue_id: str = Field(min_length=1)
    generation_version: str = Field(min_length=1)
    corpus: Any | None = None


@dataclass
class WorkerAcceptRecord:
    issue_id: str
    generation_version: str
    status: str = "accepted"


@dataclass
class WorkerIdempotencyStore:
    """In-process idempotency for Issue id + generation-version (no LLM/spend)."""

    _lock: Lock = field(default_factory=Lock)
    _records: dict[tuple[str, str], WorkerAcceptRecord] = field(default_factory=dict)

    def accept(
        self, issue_id: str, generation_version: str
    ) -> tuple[WorkerAcceptRecord, bool]:
        """Return (record, created). created=False → idempotent replay."""
        key = (issue_id, generation_version)
        with self._lock:
            existing = self._records.get(key)
            if existing is not None:
                return existing, False
            record = WorkerAcceptRecord(
                issue_id=issue_id,
                generation_version=generation_version,
                status="accepted",
            )
            self._records[key] = record
            return record, True


def accept_response_body(record: WorkerAcceptRecord, *, created: bool) -> dict[str, Any]:
    return {
        "status": record.status,
        "issue_id": record.issue_id,
        "generation_version": record.generation_version,
        "idempotent": not created,
        # Pipeline (brief/poster/bind) not run in STORY-46 — admitted only.
        "pipeline": "deferred",
    }
