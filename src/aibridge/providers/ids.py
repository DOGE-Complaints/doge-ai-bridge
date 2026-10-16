"""Provider id constants — worker slots only (REQ-10 / arch 01)."""

from __future__ import annotations

from enum import StrEnum


class ProviderId(StrEnum):
    MOCK = "mock"
    OPENAI = "openai"


ALLOWED_PROVIDER_IDS: frozenset[str] = frozenset(
    {ProviderId.MOCK.value, ProviderId.OPENAI.value}
)
