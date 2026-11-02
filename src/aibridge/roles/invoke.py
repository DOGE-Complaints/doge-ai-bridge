"""Role/model invokes via REQ-12 interview port Keep — not worker providers/."""

from __future__ import annotations

from typing import TYPE_CHECKING

from aibridge.interview import InterviewEngine
from aibridge.interview_providers.registry import bind_interview_engine_at_wire

if TYPE_CHECKING:
    from aibridge.config import Settings


def bind_role_interview_engine(
    settings: Settings,
    *,
    timeout_ms: int,
    connect_timeout_ms: int,
) -> InterviewEngine:
    """Wire role model calls through interview_providers Keep only.

    Must not import or merge into ``aibridge.providers``.
    """
    return bind_interview_engine_at_wire(
        settings,
        timeout_ms=timeout_ms,
        connect_timeout_ms=connect_timeout_ms,
    )
