"""Settings-backed provider registry — independent text/image resolve.

Unknown provider id → ProviderConfigError (AC-10-05). Never silently maps to OpenAI.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from aibridge.providers.adapters import (
    MockImagePosterProvider,
    MockTextBriefProvider,
    OpenAIImagePosterProvider,
    OpenAITextBriefProvider,
)
from aibridge.providers.errors import ProviderConfigError, ProviderFailureClass
from aibridge.providers.ids import ALLOWED_PROVIDER_IDS, ProviderId
from aibridge.providers.ports import ImagePosterProviderPort, TextBriefProviderPort

if TYPE_CHECKING:
    from aibridge.config import Settings


def normalize_provider_id(raw: str | None, *, slot: str) -> ProviderId:
    """Unset/blank → mock. Known ids → enum. Unknown → fail-closed (no OpenAI fallback)."""
    value = (raw or "").strip().lower()
    if not value:
        return ProviderId.MOCK
    if value not in ALLOWED_PROVIDER_IDS:
        raise ProviderConfigError(
            ProviderFailureClass.UNKNOWN_PROVIDER,
            f"unknown worker {slot} provider id: {value!r}",
            slot=slot,
            provider_id=value,
        )
    return ProviderId(value)


@dataclass(frozen=True)
class ProviderRegistry:
    """Independent resolvers for text-brief and image-poster slots."""

    text_provider_id: ProviderId
    image_provider_id: ProviderId
    settings: Settings | None = None

    def resolve_text(self) -> TextBriefProviderPort:
        if self.text_provider_id is ProviderId.MOCK:
            return MockTextBriefProvider()
        if self.text_provider_id is ProviderId.OPENAI:
            cfg = self.settings
            timeout = (
                int(cfg.aibridge_openai_timeout_ms)
                if cfg is not None and cfg.aibridge_openai_timeout_ms
                else 30_000
            )
            return OpenAITextBriefProvider(
                api_key=(cfg.openai_api_key if cfg is not None else "") or "",
                timeout_ms=timeout,
            )
        raise ProviderConfigError(
            ProviderFailureClass.UNKNOWN_PROVIDER,
            f"unmapped text provider: {self.text_provider_id}",
            slot="text_brief",
            provider_id=str(self.text_provider_id),
        )

    def resolve_image(self) -> ImagePosterProviderPort:
        if self.image_provider_id is ProviderId.MOCK:
            return MockImagePosterProvider()
        if self.image_provider_id is ProviderId.OPENAI:
            return OpenAIImagePosterProvider()
        raise ProviderConfigError(
            ProviderFailureClass.UNKNOWN_PROVIDER,
            f"unmapped image provider: {self.image_provider_id}",
            slot="image_poster",
            provider_id=str(self.image_provider_id),
        )


def registry_from_settings(settings: Settings) -> ProviderRegistry:
    text_id = normalize_provider_id(
        settings.aibridge_worker_text_brief_provider, slot="text_brief"
    )
    image_id = normalize_provider_id(
        settings.aibridge_worker_image_poster_provider, slot="image_poster"
    )
    return ProviderRegistry(
        text_provider_id=text_id,
        image_provider_id=image_id,
        settings=settings,
    )


def resolve_text_brief_provider(settings: Settings) -> TextBriefProviderPort:
    return registry_from_settings(settings).resolve_text()


def resolve_image_poster_provider(settings: Settings) -> ImagePosterProviderPort:
    return registry_from_settings(settings).resolve_image()
