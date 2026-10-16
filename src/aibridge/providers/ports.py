"""Selectable provider ports for worker text-brief and image-poster slots.

Accept wire = STORY-52 (mock) / STORY-54 (live openai text). Registry resolve = STORY-51.
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from aibridge.providers.ids import ProviderId


@runtime_checkable
class TextBriefProviderPort(Protocol):
    """Produce a logical L2 brief from corpus (or raise brief/provider errors)."""

    @property
    def provider_id(self) -> ProviderId:
        ...

    def generate_brief(self, corpus: dict[str, Any], *, text_brief_model: str) -> Any:
        ...


@runtime_checkable
class ImagePosterProviderPort(Protocol):
    """Produce poster bytes from a brief (or raise poster/provider errors)."""

    @property
    def provider_id(self) -> ProviderId:
        ...

    def generate_poster_bytes(self, brief: Any, *, image_poster_model: str) -> bytes:
        ...
