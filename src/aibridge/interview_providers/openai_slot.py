"""OpenAI interview slot — Keep ProductionResponsesClient behind port (STORY-59/60)."""

from __future__ import annotations

from dataclasses import dataclass

from aibridge.interview_providers.ids import InterviewProviderId
from aibridge.responses_client import ProductionResponsesClient, ResponsesClient


@dataclass(frozen=True)
class OpenAIInterviewProvider:
    """Interview port binding for provider=openai (L12-3 Keep OPENAI_* nest)."""

    api_key: str
    model: str

    @property
    def provider_id(self) -> InterviewProviderId:
        return InterviewProviderId.OPENAI

    def model_id(self) -> str:
        return self.model

    def build_client(
        self,
        *,
        timeout_ms: int,
        connect_timeout_ms: int,
    ) -> ResponsesClient:
        return ProductionResponsesClient(
            api_key=self.api_key,
            model=self.model,
            timeout_ms=timeout_ms,
            connect_timeout_ms=connect_timeout_ms,
        )
