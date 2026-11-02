"""Interview provider registry — env id → port; wire/start bind only (D4).

Must not read ``AIBRIDGE_WORKER_*_PROVIDER`` (AC-AIB-12-02).
Must not live under ``aibridge.providers``.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from aibridge.interview import InterviewEngine
from aibridge.interview_providers.deepseek_slot import DeepSeekInterviewProvider
from aibridge.interview_providers.errors import (
    InterviewProviderConfigError,
    InterviewProviderFailureClass,
)
from aibridge.interview_providers.ids import (
    ALLOWED_INTERVIEW_PROVIDER_IDS,
    InterviewProviderId,
)
from aibridge.interview_providers.openai_slot import OpenAIInterviewProvider
from aibridge.interview_providers.ports import InterviewProviderPort

if TYPE_CHECKING:
    from aibridge.config import Settings


def normalize_interview_provider_id(raw: str | None) -> InterviewProviderId:
    """Required id ∈ {deepseek, openai}. Unset/empty/unknown → fail-closed."""
    value = (raw or "").strip().lower()
    if not value:
        raise InterviewProviderConfigError(
            InterviewProviderFailureClass.MISSING,
            "AIBRIDGE_INTERVIEW_PROVIDER is required (deepseek|openai)",
            provider_id=value or None,
        )
    if value not in ALLOWED_INTERVIEW_PROVIDER_IDS:
        raise InterviewProviderConfigError(
            InterviewProviderFailureClass.UNKNOWN,
            f"unknown interview provider id: {value!r}",
            provider_id=value,
        )
    return InterviewProviderId(value)


@dataclass(frozen=True)
class InterviewProviderRegistry:
    """Map interview provider id → port (channel + REQ-13 role model path Keep)."""

    provider_id: InterviewProviderId
    port: InterviewProviderPort

    def resolve(self) -> InterviewProviderPort:
        return self.port


def port_from_settings(settings: Settings) -> InterviewProviderPort:
    """Build port after nest validation (L12-3). Does not consult worker env."""
    provider_id = normalize_interview_provider_id(settings.aibridge_interview_provider)
    if provider_id is InterviewProviderId.OPENAI:
        if not settings.openai_presence_ok():
            raise InterviewProviderConfigError(
                InterviewProviderFailureClass.INCOMPLETE,
                "openai interview nest requires OPENAI_API_KEY and OPENAI_MODEL",
                provider_id=provider_id.value,
            )
        return OpenAIInterviewProvider(
            api_key=settings.openai_api_key,
            model=settings.openai_model,
        )
    if provider_id is InterviewProviderId.DEEPSEEK:
        key = (settings.aibridge_interview_deepseek_api_key or "").strip()
        base = (settings.aibridge_interview_deepseek_base_url or "").strip()
        model = (settings.aibridge_interview_deepseek_model or "").strip()
        if not (key and base and model):
            raise InterviewProviderConfigError(
                InterviewProviderFailureClass.INCOMPLETE,
                "deepseek interview nest requires "
                "AIBRIDGE_INTERVIEW_DEEPSEEK_API_KEY, "
                "AIBRIDGE_INTERVIEW_DEEPSEEK_BASE_URL, "
                "AIBRIDGE_INTERVIEW_DEEPSEEK_MODEL",
                provider_id=provider_id.value,
            )
        return DeepSeekInterviewProvider(api_key=key, base_url=base, model=model)
    raise InterviewProviderConfigError(
        InterviewProviderFailureClass.UNKNOWN,
        f"unmapped interview provider: {provider_id}",
        provider_id=str(provider_id),
    )


def registry_from_settings(settings: Settings) -> InterviewProviderRegistry:
    port = port_from_settings(settings)
    return InterviewProviderRegistry(provider_id=port.provider_id, port=port)


def bind_interview_engine_at_wire(
    settings: Settings,
    *,
    timeout_ms: int,
    connect_timeout_ms: int,
) -> InterviewEngine:
    """Wire/start bind only (D4) — fail-closed before Responses/recording fallback.

    Recording is never a substitute for missing/unknown provider.
    """
    port = port_from_settings(settings)
    client = port.build_client(
        timeout_ms=timeout_ms,
        connect_timeout_ms=connect_timeout_ms,
    )
    return InterviewEngine(client=client, model=port.model_id())
