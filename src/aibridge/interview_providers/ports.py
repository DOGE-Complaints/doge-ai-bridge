"""Logical InterviewProviderPort — supplies Responses-compatible client for InterviewEngine.

Home: ``aibridge.interview_providers`` (must not live under ``aibridge.providers``).
Adapter HTTP bodies for DeepSeek = OOS STORY-60.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from aibridge.interview_providers.ids import InterviewProviderId
from aibridge.responses_client import ResponsesClient


@runtime_checkable
class InterviewProviderPort(Protocol):
    """Resolve backend client for Keep InterviewEngine (Interview D3)."""

    @property
    def provider_id(self) -> InterviewProviderId:
        ...

    def model_id(self) -> str:
        ...

    def build_client(
        self,
        *,
        timeout_ms: int,
        connect_timeout_ms: int,
    ) -> ResponsesClient:
        ...
