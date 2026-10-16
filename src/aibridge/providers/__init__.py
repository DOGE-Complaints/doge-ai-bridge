"""Worker AI provider registry + ports (STORY-AIBRIDGE-51 / REQ-10).

Channel/interview OpenAI client is out of scope (L10-1). Accept-pipe mock wire = STORY-52;
readyz allow-mock = STORY-53; live OpenAI text invoke = STORY-54.
"""

from aibridge.providers.errors import ProviderConfigError, ProviderFailureClass
from aibridge.providers.ids import ALLOWED_PROVIDER_IDS, ProviderId
from aibridge.providers.ports import ImagePosterProviderPort, TextBriefProviderPort
from aibridge.providers.registry import (
    ProviderRegistry,
    registry_from_settings,
    resolve_image_poster_provider,
    resolve_text_brief_provider,
)

__all__ = [
    "ALLOWED_PROVIDER_IDS",
    "ImagePosterProviderPort",
    "ProviderConfigError",
    "ProviderFailureClass",
    "ProviderId",
    "ProviderRegistry",
    "TextBriefProviderPort",
    "registry_from_settings",
    "resolve_image_poster_provider",
    "resolve_text_brief_provider",
]
