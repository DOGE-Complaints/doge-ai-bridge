"""Provider config / resolve failures — fail-closed, no silent OpenAI fallback."""

from __future__ import annotations

from enum import StrEnum


class ProviderFailureClass(StrEnum):
    UNKNOWN_PROVIDER = "unknown_provider"
    INCOMPLETE_PROVIDER_CONFIG = "incomplete_provider_config"


class ProviderConfigError(Exception):
    """Raised when provider id/config cannot be resolved safely."""

    def __init__(
        self,
        failure_class: ProviderFailureClass,
        message: str,
        *,
        slot: str | None = None,
        provider_id: str | None = None,
    ) -> None:
        super().__init__(message)
        self.failure_class = failure_class
        self.slot = slot
        self.provider_id = provider_id
