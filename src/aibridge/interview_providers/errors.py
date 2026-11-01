"""Interview provider failures — config fail-closed vs vendor/transport.

Literals are typed enums only (fail-reason string SSOT = Open / OOS).
"""

from __future__ import annotations

from enum import StrEnum

from aibridge.responses_client import ResponsesTransportError


class InterviewProviderFailureClass(StrEnum):
    MISSING = "interview_provider_missing"
    UNKNOWN = "interview_provider_unknown"
    INCOMPLETE = "interview_provider_incomplete"
    ADAPTER_DEFERRED = "interview_adapter_deferred"  # historical STORY-59; unused after 60
    VENDOR_TRANSPORT = "interview_provider_vendor_transport"


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


class InterviewProviderTransportError(ResponsesTransportError):
    """Vendor/HTTP/timeout from interview adapter — Engine-safe (ResponsesTransportError)."""

    failure_class = InterviewProviderFailureClass.VENDOR_TRANSPORT

    def __init__(
        self,
        outcome: str,
        message: str,
        *,
        provider_id: str | None = None,
    ) -> None:
        super().__init__(outcome, message)
        self.provider_id = provider_id
