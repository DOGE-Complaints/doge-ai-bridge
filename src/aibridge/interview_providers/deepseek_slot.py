"""DeepSeek interview slot — nest validated; HTTP adapter body OOS STORY-60."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from aibridge.interview_providers.errors import (
    InterviewProviderConfigError,
    InterviewProviderFailureClass,
)
from aibridge.interview_providers.ids import InterviewProviderId
from aibridge.responses_client import ResponsesClient, ResponsesRequest


@dataclass(frozen=True)
class DeferredDeepSeekInterviewClient:
    """Bound at wire/start (D4) — create/acreate refuse until STORY-60 adapter."""

    api_key: str
    base_url: str
    model: str

    def create(self, request: ResponsesRequest) -> dict[str, Any]:
        raise InterviewProviderConfigError(
            InterviewProviderFailureClass.ADAPTER_DEFERRED,
            "deepseek interview adapter HTTP body deferred to STORY-60",
            provider_id=InterviewProviderId.DEEPSEEK.value,
        )

    async def acreate(self, request: ResponsesRequest) -> dict[str, Any]:
        raise InterviewProviderConfigError(
            InterviewProviderFailureClass.ADAPTER_DEFERRED,
            "deepseek interview adapter HTTP body deferred to STORY-60",
            provider_id=InterviewProviderId.DEEPSEEK.value,
        )


@dataclass(frozen=True)
class DeepSeekInterviewProvider:
    """Interview port binding for provider=deepseek (L12-3 nest required)."""

    api_key: str
    base_url: str
    model: str

    @property
    def provider_id(self) -> InterviewProviderId:
        return InterviewProviderId.DEEPSEEK

    def model_id(self) -> str:
        return self.model

    def build_client(
        self,
        *,
        timeout_ms: int,
        connect_timeout_ms: int,
    ) -> ResponsesClient:
        del timeout_ms, connect_timeout_ms  # reserved for STORY-60 adapter
        return DeferredDeepSeekInterviewClient(
            api_key=self.api_key,
            base_url=self.base_url,
            model=self.model,
        )
