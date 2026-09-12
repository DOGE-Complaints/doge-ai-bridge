"""STORY-AIBRIDGE-06 — metrics, audit, ops paths, wave-1 smoke, env knobs."""

from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from aibridge.app import create_app
from aibridge.audit import get_audit_buffer, reset_audit_buffer
from aibridge.budgets import BudgetBreachError, BudgetGuard, BudgetLimits
from aibridge.config import Settings, reset_settings_cache
from aibridge.confirm import reset_confirmation_guard
from aibridge.dedupe import EventDedupeStore
from aibridge.metrics import assert_no_narrative_in_metrics, get_metrics, reset_metrics

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT  # doge-ai-bridge/


def _client() -> TestClient:
    reset_settings_cache()
    reset_confirmation_guard()
    reset_metrics()
    reset_audit_buffer()
    settings = Settings(
        AIBRIDGE_CHANNEL_BEARER_TOKEN="channel-token-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        DOGESTONIA_API_BEARER_TOKEN="gateway-token-bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
        DOGESTONIA_GATEWAY_ORIGIN="https://gateway.example.invalid",
        AIBRIDGE_DRY_RUN=True,
    )
    app = create_app(settings=settings, dedupe_store=EventDedupeStore())
    return TestClient(app)


def test_metrics_without_bearer_no_narrative() -> None:
    client = _client()
    phrase = "UNIQUE_PRIVACY_PHRASE_ZX9Q_NEVER_IN_METRICS"
    headers = {
        "Authorization": "Bearer channel-token-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    }
    r = client.post(
        "/v1/channel/turns",
        json={
            "channel": "telegram",
            "event_id": "ops-m1",
            "principal": {"user_id": "1", "chat_id": "2"},
            "message": {"message_id": "9", "text": phrase},
        },
        headers=headers,
    )
    assert r.status_code == 200
    metrics = client.get("/metrics")
    assert metrics.status_code == 200
    body = metrics.text
    assert "aibridge_channel_turns_total" in body
    assert_no_narrative_in_metrics(body, sample=phrase)
    assert "Bearer " not in body
    assert phrase not in body


def test_budget_stop_reason_in_metrics() -> None:
    reset_metrics()
    g = BudgetGuard(BudgetLimits(max_session_turns=0))
    try:
        g.check_turn_start("s1")
    except BudgetBreachError:
        pass
    text = get_metrics().render_prometheus()
    assert 'aibridge_budget_stops_total{reason="budget_session_turns"}' in text


def test_privacy_phrase_absent_from_audit_and_metrics() -> None:
    client = _client()
    phrase = "UNIQUE_AUDIT_PHRASE_Y7K_ABSENT"
    headers = {
        "Authorization": "Bearer channel-token-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    }
    client.post(
        "/v1/channel/turns",
        json={
            "channel": "telegram",
            "event_id": "ops-a1",
            "principal": {"user_id": "1", "chat_id": "2"},
            "message": {"message_id": "1", "text": phrase},
        },
        headers=headers,
    )
    audit_text = get_audit_buffer().dump_text()
    assert phrase not in audit_text
    assert phrase not in client.get("/metrics").text


def test_runbook_and_ops_paths_exist() -> None:
    paths = [
        REPO / "docs/runbooks/privacy-pilot.md",
        REPO / "docs/runbooks/unknown-outcome-reconciliation.md",
        REPO / "docs/runbooks/channel-bearer-rotation.md",
        REPO / "docs/ops/n8n-channel-workflow/README.md",
        REPO / "docs/ops/operator-pilot-readme.md",
        REPO / "docs/ops/wave1-gate-checklist.md",
    ]
    missing = [str(p) for p in paths if not p.is_file()]
    assert missing == [], missing


def test_wave1_readyz_and_401_smoke() -> None:
    client = _client()
    ready = client.get("/readyz")
    assert ready.status_code == 200
    assert ready.json()["status"] == "ready"
    unauth = client.post(
        "/v1/channel/turns",
        json={
            "channel": "telegram",
            "event_id": "ops-401",
            "principal": {"user_id": "1", "chat_id": "2"},
            "message": {"message_id": "1", "text": "x"},
        },
    )
    assert unauth.status_code == 401


def test_env_example_lists_required_knobs_without_secrets() -> None:
    text = (REPO / ".env.example").read_text(encoding="utf-8")
    required = [
        "PORT",
        "DATABASE_URL",
        "OPENAI_API_KEY",
        "OPENAI_MODEL",
        "OPENAI_STORE_RESPONSES",
        "DOGESTONIA_INSTRUCTIONS_DIR",
        "DOGESTONIA_API_BEARER_TOKEN",
        "DOGESTONIA_DRAFT_REDIRECT_BASE_URL",
        "AIBRIDGE_CHANNEL_BEARER_TOKEN",
        "AIBRIDGE_MAX_REQUEST_BYTES",
        "AIBRIDGE_MAX_INPUT_TOKENS",
        "AIBRIDGE_DRY_RUN",
        "DOGESTONIA_GATEWAY_ORIGIN",
    ]
    for name in required:
        assert name in text, name
    # No obvious secret literals (long hex/token shapes as assigned values).
    for line in text.splitlines():
        if "=" not in line or line.strip().startswith("#"):
            continue
        key, _, val = line.partition("=")
        val = val.strip()
        if not val:
            continue
        assert "sk-" not in val
        assert len(val) < 80 or "example" in val or "sqlite" in val or "false" in val.lower()
