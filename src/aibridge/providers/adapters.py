"""Port adapters — Present mock backends + OpenAI text live (STORY-54).

Mock adapters delegate to Present deterministic pipelines (no third fake path).
Accept orchestration wires these ports (STORY-52). Live image deferred (L10-5).
"""

from __future__ import annotations

from typing import Any, Callable

from aibridge.poster.image import generate_poster_bytes
from aibridge.providers.ids import ProviderId
from aibridge.providers.openai_text_live import extract_brief_from_stories
from aibridge.responses_client import ResponsesHttpTransport
from aibridge.sense_brief.pipeline import generate_sense_brief

InvokeFn = Callable[[dict[str, Any]], dict[str, Any]]


class MockTextBriefProvider:
    """Present corpus-grounded brief path behind the text port (L10-3)."""

    @property
    def provider_id(self) -> ProviderId:
        return ProviderId.MOCK

    def generate_brief(self, corpus: dict[str, Any], *, text_brief_model: str) -> Any:
        return generate_sense_brief(corpus, text_brief_model=text_brief_model or "mock")


class OpenAITextBriefProvider:
    """Live OpenAI text extract from gateway ``{stories:[…]}`` → L2 (AC-10-10)."""

    def __init__(
        self,
        *,
        api_key: str = "",
        transport: ResponsesHttpTransport | None = None,
        invoke: InvokeFn | None = None,
        timeout_ms: int = 30_000,
        connect_timeout_ms: int = 5_000,
    ) -> None:
        self._api_key = api_key
        self._transport = transport
        self._invoke = invoke
        self._timeout_ms = timeout_ms
        self._connect_timeout_ms = connect_timeout_ms

    @property
    def provider_id(self) -> ProviderId:
        return ProviderId.OPENAI

    def generate_brief(self, corpus: dict[str, Any], *, text_brief_model: str) -> Any:
        return extract_brief_from_stories(
            corpus,
            text_brief_model=text_brief_model,
            api_key=self._api_key,
            transport=self._transport,
            invoke=self._invoke,
            timeout_ms=self._timeout_ms,
            connect_timeout_ms=self._connect_timeout_ms,
        )


class MockImagePosterProvider:
    """Present deterministic PNG path behind the image port (L10-4)."""

    @property
    def provider_id(self) -> ProviderId:
        return ProviderId.MOCK

    def generate_poster_bytes(self, brief: Any, *, image_poster_model: str) -> bytes:
        return generate_poster_bytes(
            brief, image_poster_model=image_poster_model or "mock"
        )


class OpenAIImagePosterProvider:
    """Resolved openai image port — live image vendor deferred (L10-5)."""

    @property
    def provider_id(self) -> ProviderId:
        return ProviderId.OPENAI

    def generate_poster_bytes(self, brief: Any, *, image_poster_model: str) -> bytes:
        raise NotImplementedError(
            "live image-poster provider invoke deferred — not this story (accept wire is mock-path)"
        )
