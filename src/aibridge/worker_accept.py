"""Sense-brief worker accept — entry/auth/idempotency + brief pipeline hook.

Implement names (Open in arch; chosen for this wave, documented in task READMEs):
- Path: ``POST /v1/worker/sense-brief/accept``
- Prefix: ``/v1/worker/``
- Env: ``AIBRIDGE_WORKER_SENSE_BRIEF_ENABLED``, ``AIBRIDGE_WORKER_SENSE_BRIEF_S2S_TOKEN``,
  ``AIBRIDGE_WORKER_TEXT_BRIEF_MODEL`` (STORY-47),
  ``AIBRIDGE_WORKER_IMAGE_POSTER_MODEL``, ``AIBRIDGE_WORKER_STORAGE_UPLOAD_CREDENTIAL`` (STORY-48)
- JSON: ``issue_id``, ``generation_version``, optional ``corpus``
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
    brief: dict[str, Any] | None = None
    poster_url: str | None = None
    pipeline: str = "deferred"


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

    def store_brief(
        self,
        issue_id: str,
        generation_version: str,
        brief: dict[str, Any],
        *,
        pipeline: str = "brief_ready",
        poster_url: str | None = None,
    ) -> WorkerAcceptRecord:
        key = (issue_id, generation_version)
        with self._lock:
            record = self._records.get(key)
            if record is None:
                record = WorkerAcceptRecord(
                    issue_id=issue_id,
                    generation_version=generation_version,
                )
                self._records[key] = record
            record.brief = brief
            if poster_url is not None:
                record.poster_url = poster_url
            record.pipeline = pipeline
            record.status = "accepted"
            return record


def accept_response_body(record: WorkerAcceptRecord, *, created: bool) -> dict[str, Any]:
    body: dict[str, Any] = {
        "status": record.status,
        "issue_id": record.issue_id,
        "generation_version": record.generation_version,
        "idempotent": not created,
        "pipeline": record.pipeline,
    }
    if record.brief is not None:
        body["brief"] = record.brief
    if record.poster_url is not None:
        body["poster_url"] = record.poster_url
    return body
