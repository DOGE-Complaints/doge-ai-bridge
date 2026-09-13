"""P6 audit G-01/G-02 — settings knobs enforceable + readyz strict tool."""

from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from pathlib import Path

from fastapi.testclient import TestClient

from aibridge.action_tokens import ActionTokenStore, TokenActionKind
from aibridge.app import create_app
from aibridge.budgets import budget_limits_from_settings
from aibridge.config import Settings, reset_settings_cache
from aibridge.dedupe import EventDedupeStore
from aibridge.gateway import GatewayOutcome, RecordingGatewayTransport, default_executor_from_settings
from aibridge.interview import default_recording_engine
from aibridge.rate_limit import RateLimiter
from aibridge.readiness import _strict_tool_ok, evaluate_readiness
from aibridge.sessions import MemorySessionStore

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "content"
WIRE_OAS = (
    Path(__file__).resolve().parents[1]
    / "docs"
    / "openapi"
    / "story-intake-actions.openapi.yaml"
)


def _base(**overrides: object) -> Settings:
    reset_settings_cache()
    base: dict[str, object] = dict(
        AIBRIDGE_CHANNEL_BEARER_TOKEN="channel-token-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        DOGESTONIA_API_BEARER_TOKEN="gateway-token-bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
        DOGESTONIA_API_BASE_URL="https://gateway.example.invalid",
        DOGESTONIA_DRAFT_REDIRECT_BASE_URL="https://spa.example.invalid",
        OPENAI_API_KEY="sk-test-not-real",
        OPENAI_MODEL="gpt-test",
        AIBRIDGE_DRY_RUN=True,
    )
    base.update(overrides)
    return Settings(**base)


def test_budget_limits_from_settings_when_set() -> None:
    settings = _base(
        AIBRIDGE_MAX_SESSION_TURNS=2,
        AIBRIDGE_MAX_INPUT_TOKENS=100,
        AIBRIDGE_OPENAI_TIMEOUT_MS=1500,
    )
    limits = budget_limits_from_settings(settings)
    assert limits.max_session_turns == 2
    assert limits.max_input_tokens == 100
    assert limits.openai_timeout_ms == 1500


def test_create_app_wires_budget_guard_and_token_ttl() -> None:
    settings = _base(
        AIBRIDGE_MAX_SESSION_TURNS=1,
        AIBRIDGE_ACTION_TOKEN_TTL_SECONDS=42,
    )
    app = create_app(
        settings=settings,
        dedupe_store=EventDedupeStore(),
        interview_engine=default_recording_engine(),
    )
    assert app.state.budget_guard is not None
    assert app.state.budget_guard.limits.max_session_turns == 1
    assert app.state.confirmation_guard.tokens.ttl_seconds == 42


def test_action_token_ttl_from_settings_expires() -> None:
    store = ActionTokenStore(ttl_seconds=1)
    raw, rec = store.issue(
        action=TokenActionKind.CONFIRM_SEND,
        session_id="s1",
        user_id="u",
        chat_id="c",
        deployment_id="d",
        revision=1,
        expected_state="awaiting_send",
        now=100.0,
    )
    assert rec.expires_at == 101.0
    assert store.lookup(raw).expires_at == 101.0


def test_http_total_timeout_and_max_response_bytes_on_gateway() -> None:
    settings = _base(
        AIBRIDGE_HTTP_TOTAL_TIMEOUT_MS=2500,
        AIBRIDGE_MAX_RESPONSE_BYTES=8,
        AIBRIDGE_DRY_RUN=False,
        AIBRIDGE_SCHEMA_VALIDATION_COMPLETE=True,
    )
    from aibridge.gateway import RawHttpResponse

    transport = RecordingGatewayTransport(
        scripted=[
            RawHttpResponse(
                status_code=201,
                body=b'{"draft_id":"x","trace_id":"t"}',
                final_url="https://gateway.example.invalid/story-drafts",
            )
        ]
    )
    ex = default_executor_from_settings(settings, transport=transport)
    assert ex.timeout_seconds == 2.5
    assert ex.max_response_bytes == 8
    assert ex.dry_run is False
    result = ex.execute_stash({"ok": True}, gateway_authorized=True)
    assert result.outcome is GatewayOutcome.CONTRACT_MISMATCH


def test_log_level_applied() -> None:
    settings = _base(AIBRIDGE_LOG_LEVEL="WARNING")
    create_app(
        settings=settings,
        dedupe_store=EventDedupeStore(),
        interview_engine=default_recording_engine(),
    )
    assert logging.getLogger("aibridge").level == logging.WARNING


def test_session_ttl_deactivates_stale_memory_session() -> None:
    store = MemorySessionStore(ttl_seconds=1)
    row = store.create(
        session_id="s-ttl",
        content_bundle_hash="h",
        deployment_id="d",
    )
    # Force stale updated_at
    store._rows["s-ttl"] = type(row)(
        session_id=row.session_id,
        content_bundle_hash=row.content_bundle_hash,
        deployment_id=row.deployment_id,
        active=True,
        created_at=row.created_at,
        updated_at=datetime.now(timezone.utc) - timedelta(seconds=10),
    )
    got = store.get("s-ttl")
    assert got is not None
    assert got.active is False


def test_rate_limiter_blocks_when_set() -> None:
    lim = RateLimiter(principal_limit=1, global_limit=None, window_seconds=60.0)
    assert lim.allow("p1") is None
    assert lim.allow("p1") == "principal_rate_limit"


def test_channel_rate_limit_429() -> None:
    settings = _base(AIBRIDGE_PRINCIPAL_RATE_LIMIT=1)
    client = TestClient(
        create_app(
            settings=settings,
            dedupe_store=EventDedupeStore(),
            interview_engine=default_recording_engine(),
        )
    )
    headers = {
        "Authorization": "Bearer channel-token-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    }
    payload = {
        "channel": "telegram",
        "event_id": "rl-1",
        "principal": {"user_id": "1", "chat_id": "2"},
        "message": {"message_id": "1", "text": "a"},
    }
    assert client.post("/v1/channel/turns", json=payload, headers=headers).status_code == 200
    payload["event_id"] = "rl-2"
    r2 = client.post("/v1/channel/turns", json=payload, headers=headers)
    assert r2.status_code == 429
    assert r2.json()["error"]["code"] == "rate_limited"


def test_strict_tool_ok_when_schema_ids_and_fixtures() -> None:
    settings = _base(
        DOGESTONIA_INSTRUCTIONS_DIR=str(FIXTURES / "instructions"),
        DOGESTONIA_INSTRUCTIONS_MANIFEST=str(FIXTURES / "instructions.manifest.json"),
        DOGESTONIA_CONTENT_SOURCE_COMMIT="ready-commit",
        DOGESTONIA_OPENAPI_PATH=str(WIRE_OAS),
        DOGESTONIA_PAYLOAD_SCHEMA_PATH=str(FIXTURES / "pack" / "payload.schema.json"),
        DOGESTONIA_SCHEMA_ID="pack-test",
        DOGESTONIA_SCHEMA_VERSION="1",
    )
    result = _strict_tool_ok(settings, deployment=None)
    assert result.ready is True


def test_strict_tool_fails_on_bad_pack() -> None:
    settings = _base(
        DOGESTONIA_INSTRUCTIONS_DIR=str(FIXTURES / "instructions"),
        DOGESTONIA_INSTRUCTIONS_MANIFEST=str(FIXTURES / "instructions.manifest.json"),
        DOGESTONIA_CONTENT_SOURCE_COMMIT="ready-commit",
        DOGESTONIA_OPENAPI_PATH=str(WIRE_OAS),
        DOGESTONIA_PAYLOAD_SCHEMA_PATH=str(FIXTURES / "pack" / "missing.json"),
        DOGESTONIA_SCHEMA_ID="pack-test",
        DOGESTONIA_SCHEMA_VERSION="1",
    )
    result = _strict_tool_ok(settings, deployment=None)
    assert result.ready is False
    assert result.reason and result.reason.startswith("tool_gen_failed:")
