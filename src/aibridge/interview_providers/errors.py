"""Interview provider config failures — fail-closed, no silent OpenAI."""

from __future__ import annotations

from enum import StrEnum


class InterviewProviderFailureClass(StrEnum):
    MISSING = "interview_provider_missing"
    UNKNOWN = "interview_provider_unknown"
    INCOMPLETE = "interview_provider_incomplete"
    ADAPTER_DEFERRED = "interview_adapter_deferred"


class InterviewProviderConfigError(Exception):
    """Raised when interview provider id/nest cannot be resolved safely."""

    def __init__(
        self,
        failure_class: InterviewProviderFailureClass,
        message: str,
        *,
        provider_id: str | None = None,
    ) -> None:
        super().__init__(message)
        self.failure_class = failure_class
        self.provider_id = provider_id
