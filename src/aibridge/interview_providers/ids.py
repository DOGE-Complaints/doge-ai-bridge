"""Interview provider ids (REQ-12 L12-1) — orthogonal to worker ProviderId."""

from __future__ import annotations

from enum import StrEnum


class InterviewProviderId(StrEnum):
    OPENAI = "openai"
    DEEPSEEK = "deepseek"


ALLOWED_INTERVIEW_PROVIDER_IDS: frozenset[str] = frozenset(
    {InterviewProviderId.OPENAI.value, InterviewProviderId.DEEPSEEK.value}
)
