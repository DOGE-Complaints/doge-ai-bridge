"""Port adapters — resolve targets for registry (no accept-pipe wire here).

Mock adapters delegate to Present deterministic pipelines.
OpenAI adapters are resolve placeholders until STORY-54 (text) / later image lock.
"""

from __future__ import annotations

from typing import Any

from aibridge.poster.image import generate_poster_bytes
from aibridge.providers.ids import ProviderId
from aibridge.sense_brief.pipeline import generate_sense_brief


class MockTextBriefProvider:
    """Present corpus-grounded brief path behind the text port (L10-3)."""

    @property
    def provider_id(self) -> ProviderId:
        return ProviderId.MOCK

    def generate_brief(self, corpus: dict[str, Any], *, text_brief_model: str) -> Any:
        return generate_sense_brief(corpus, text_brief_model=text_brief_model or "mock")


class OpenAITextBriefProvider:
    """Resolved openai text port — live HTTP invoke is STORY-54."""

    @property
    def provider_id(self) -> ProviderId:
        return ProviderId.OPENAI

    def generate_brief(self, corpus: dict[str, Any], *, text_brief_model: str) -> Any:
        raise NotImplementedError(
            "live OpenAI text brief invoke is STORY-AIBRIDGE-54 — not this story"
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
            "live image-poster provider invoke deferred — not STORY-AIBRIDGE-51"
        )
