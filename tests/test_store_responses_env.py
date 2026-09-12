"""G-03 — OPENAI_STORE_RESPONSES hygiene."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from aibridge.config import Settings, reset_settings_cache


def test_openai_store_responses_true_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    reset_settings_cache()
    monkeypatch.setenv("OPENAI_STORE_RESPONSES", "true")
    with pytest.raises(ValidationError, match="store:false"):
        Settings()


def test_openai_store_responses_false_ok(monkeypatch: pytest.MonkeyPatch) -> None:
    reset_settings_cache()
    monkeypatch.setenv("OPENAI_STORE_RESPONSES", "false")
    s = Settings()
    assert s.responses_store_false_enforced() is True
