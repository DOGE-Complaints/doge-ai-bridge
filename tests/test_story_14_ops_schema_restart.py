"""STORY-AIBRIDGE-14 — ops shutdown, budgets/rate defaults, schema, restart races, knobs, Dockerfile."""

from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from aibridge.app import create_app
from aibridge.budgets import BudgetGuard, budget_limits_from_settings
from aibridge.config import (
    DEFAULT_GLOBAL_RATE_LIMIT,
    DEFAULT_MAX_RESPONSE_BYTES,
    DEFAULT_MAX_RESPONSES_CALLS_PER_TURN,
    DEFAULT_PRINCIPAL_RATE_LIMIT,
    Settings,
    reset_settings_cache,
)
from aibridge.confirm import ConfirmationGuard, ConfirmSession
from aibridge.confirm_fsm import SessionState
from aibridge.dedupe import EventDedupeStore
from aibridge.gateway import (
    GatewayOutcome,
    GatewayResult,
    RawHttpResponse,
    RecordingGatewayTransport,
    default_executor_from_settings,
)
from aibridge.interview import default_recording_engine
from aibridge.readiness import evaluate_readiness
from aibridge.request_assembly import (
    ValidationGateError,
    schema_validation_complete,
    validate_gate1_tool_args,
    validate_gate2_pack_payload,
)


def _ready_settings(**overrides: object) -> Settings:
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


def _sess(**kwargs: object) -> ConfirmSession:
    base: dict[str, object] = dict(
        session_id="s1",
        user_id="u",
        chat_id="c",
        deployment_id="local",
    )
    base.update(kwargs)
    return ConfirmSession(**base)  # type: ignore[arg-type]


def test_story_14_drain_rejects_new_channel_turns() -> None:
    settings = _ready_settings()
    app = create_app(settings=settings, dedupe_store=EventDedupeStore())
    client = TestClient(app)
    assert app.state.accepting_traffic is True
    app.state.accepting_traffic = False
    r = client.post(
        "/v1/channel/turns",
        json={
            "channel": "telegram",
            "event_id": "drain-1",
            "principal": {"user_id": "1", "chat_id": "2"},
            "message": {"message_id": "10", "text": "hi"},
        },
        headers={"Authorization": "Bearer channel-token-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"},
    )
    assert r.status_code == 503
    assert r.json()["error"]["code"] == "shutting_down"
    assert client.get("/healthz").status_code == 200


def test_story_14_lifespan_marks_executing_unknown_on_shutdown() -> None:
    settings = _ready_settings()

    class _Attempts:
        def __init__(self) -> None:
            self.rows = [{"session_id": "s-drain", "revision": 2}]
            self.outcomes: list[str] = []

        def list_executing(self) -> list[dict]:
            return list(self.rows)

        def get(self, *, session_id: str, revision: int) -> dict | None:
            for row in self.rows:
                if row["session_id"] == session_id and int(row["revision"]) == revision:
                    return {"status": "executing", **row}
            return None

        def set_outcome(self, *, session_id: str, revision: int, outcome: str) -> None:
            self.outcomes.append(outcome)
            self.rows = [
                r
                for r in self.rows
                if not (r["session_id"] == session_id and int(r["revision"]) == revision)
            ]

    attempts = _Attempts()
    guard = ConfirmationGuard(
        executor=default_executor_from_settings(settings),
        gateway_attempts=attempts,  # type: ignore[arg-type]
    )
    sess = _sess(session_id="s-drain", state=SessionState.EXECUTING, revision=2)
    guard._sessions[sess.session_id] = sess  # noqa: SLF001

    with TestClient(
        create_app(
            settings=settings,
            dedupe_store=EventDedupeStore(),
            confirmation_guard=guard,
        )
    ) as client:
        assert client.app.state.accepting_traffic is True
    assert GatewayOutcome.UNKNOWN_OUTCOME.value in attempts.outcomes
    assert sess.state is SessionState.UNKNOWN_OUTCOME


def test_story_14_finite_budget_and_rate_defaults() -> None:
    settings = _ready_settings()
    assert settings.aibridge_principal_rate_limit == DEFAULT_PRINCIPAL_RATE_LIMIT
    assert settings.aibridge_global_rate_limit == DEFAULT_GLOBAL_RATE_LIMIT
    assert (
        settings.aibridge_max_responses_calls_per_turn
        == DEFAULT_MAX_RESPONSES_CALLS_PER_TURN
    )
    limits = budget_limits_from_settings(settings)
    assert limits.max_responses_calls_per_turn == DEFAULT_MAX_RESPONSES_CALLS_PER_TURN
    app = create_app(settings=settings, dedupe_store=EventDedupeStore())
    assert app.state.budget_guard is not None
    assert isinstance(app.state.budget_guard, BudgetGuard)
    assert app.state.rate_limiter.enabled()


def test_story_14_budget_enforced_on_turns_session_cap() -> None:
    settings = _ready_settings(AIBRIDGE_MAX_SESSION_TURNS=1)
    app = create_app(
        settings=settings,
        dedupe_store=EventDedupeStore(),
        interview_engine=default_recording_engine(),
    )
    # Attach budget guard after recording engine factory (create_app also wires budgets).
    assert app.state.budget_guard is not None
    app.state.interview_engine.budgets = BudgetGuard(
        budget_limits_from_settings(settings)
    )
    client = TestClient(app)
    headers = {
        "Authorization": "Bearer channel-token-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    }
    body = {
        "channel": "telegram",
        "event_id": "budget-turn-1",
        "principal": {"user_id": "11", "chat_id": "22"},
        "message": {"message_id": "1", "text": "first"},
    }
    r1 = client.post("/v1/channel/turns", json=body, headers=headers)
    assert r1.status_code == 200
    body2 = {
        **body,
        "event_id": "budget-turn-2",
        "message": {"message_id": "2", "text": "second"},
    }
    r2 = client.post("/v1/channel/turns", json=body2, headers=headers)
    assert r2.status_code == 200
    assert "budget" in (r2.json().get("reply_text") or "").lower()


def test_story_14_channel_rate_limit_429_with_defaults_overridden() -> None:
    settings = _ready_settings(
        AIBRIDGE_PRINCIPAL_RATE_LIMIT=1,
        AIBRIDGE_GLOBAL_RATE_LIMIT=1000,
    )
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
    body = {
        "channel": "telegram",
        "event_id": "rl-1",
        "principal": {"user_id": "1", "chat_id": "2"},
        "message": {"message_id": "1", "text": "a"},
    }
    assert client.post("/v1/channel/turns", json=body, headers=headers).status_code == 200
    body2 = {**body, "event_id": "rl-2"}
    r2 = client.post("/v1/channel/turns", json=body2, headers=headers)
    assert r2.status_code == 429
    assert r2.json()["error"]["code"] == "rate_limited"


def test_story_14_enum_validation_rejects_and_accepts() -> None:
    assert schema_validation_complete() is True
    schema = {
        "type": "object",
        "properties": {"tone": {"type": "string", "enum": ["formal", "casual"]}},
        "required": ["tone"],
    }
    validate_gate2_pack_payload({"tone": "formal"}, schema)
    with pytest.raises(ValidationGateError) as ei:
        validate_gate2_pack_payload({"tone": "slang"}, schema)
    assert "enum" in str(ei.value)


def test_story_14_const_and_bounds() -> None:
    validate_gate1_tool_args(
        {"n": 3},
        {
            "type": "object",
            "properties": {"n": {"type": "integer", "minimum": 1, "maximum": 5}},
            "required": ["n"],
        },
    )
    with pytest.raises(ValidationGateError):
        validate_gate1_tool_args(
            {"n": 9},
            {
                "type": "object",
                "properties": {"n": {"type": "integer", "maximum": 5}},
                "required": ["n"],
            },
        )
    validate_gate1_tool_args(
        {"k": "fixed"},
        {
            "type": "object",
            "properties": {"k": {"const": "fixed"}},
            "required": ["k"],
        },
    )


def test_story_14_readyz_dry_run_false_after_schema_complete() -> None:
    blocked = _ready_settings(
        AIBRIDGE_DRY_RUN=False,
        AIBRIDGE_SCHEMA_VALIDATION_COMPLETE=False,
    )
    assert evaluate_readiness(blocked).ready is False
    assert evaluate_readiness(blocked).reason == "dry_run_required"

    ok = _ready_settings(
        AIBRIDGE_DRY_RUN=False,
        AIBRIDGE_SCHEMA_VALIDATION_COMPLETE=True,
    )
    assert evaluate_readiness(ok).ready is True
    client = TestClient(create_app(settings=ok, dedupe_store=EventDedupeStore()))
    assert client.get("/readyz").status_code == 200


def test_story_14_restart_recover_all_no_auto_resend() -> None:
    settings = _ready_settings()
    transport = RecordingGatewayTransport(
        scripted=[RawHttpResponse(status_code=201, body=b'{"data":{"draft_id":"d1"}}')]
    )
    executor = default_executor_from_settings(settings, transport=transport)

    class _Attempts:
        def __init__(self) -> None:
            self._row: dict = {
                "session_id": "s-race",
                "revision": 1,
                "status": "executing",
            }

        def list_executing(self) -> list[dict]:
            return [dict(self._row)] if self._row.get("status") == "executing" else []

        def get(self, *, session_id: str, revision: int) -> dict | None:
            if (
                self._row.get("session_id") == session_id
                and int(self._row.get("revision") or 0) == revision
            ):
                return dict(self._row)
            return None

        def set_outcome(self, *, session_id: str, revision: int, outcome: str) -> None:
            self._row["status"] = outcome
            self._row["outcome"] = outcome

    attempts = _Attempts()
    guard = ConfirmationGuard(executor=executor, gateway_attempts=attempts)  # type: ignore[arg-type]
    sess = _sess(
        session_id="s-race",
        state=SessionState.EXECUTING,
        revision=1,
        gateway_authorized=True,
    )
    guard._sessions[sess.session_id] = sess  # noqa: SLF001
    n = guard.recover_all_executing_attempts()
    assert n == 1
    assert sess.state is SessionState.UNKNOWN_OUTCOME
    assert guard.send_blocked_for_revision(sess) is True
    assert transport.calls == []


def test_story_14_pending_confirm_blocks_send_after_unknown() -> None:
    settings = _ready_settings()
    guard = ConfirmationGuard(executor=default_executor_from_settings(settings))
    sess = _sess(
        session_id="s-pc",
        state=SessionState.AWAITING_SEND_CONFIRM,
        revision=4,
        unknown_outcome_revision=4,
    )
    guard._sessions[sess.session_id] = sess  # noqa: SLF001
    assert guard.send_blocked_for_revision(sess) is True


def test_story_14_unknown_outcome_mapping_from_timeout() -> None:
    settings = _ready_settings(AIBRIDGE_DRY_RUN=False)
    transport = RecordingGatewayTransport(raise_on_call=TimeoutError("connect timeout"))
    ex = default_executor_from_settings(settings, transport=transport)
    result = ex.execute_stash({"x": 1}, gateway_authorized=True)
    assert isinstance(result, GatewayResult)
    assert result.outcome is GatewayOutcome.UNKNOWN_OUTCOME


def test_story_14_max_response_bytes_default_and_enforce() -> None:
    settings = _ready_settings(AIBRIDGE_DRY_RUN=False)
    assert settings.aibridge_max_response_bytes == DEFAULT_MAX_RESPONSE_BYTES
    transport = RecordingGatewayTransport(
        scripted=[
            RawHttpResponse(
                status_code=201,
                body=b"x" * (DEFAULT_MAX_RESPONSE_BYTES + 1),
            )
        ]
    )
    ex = default_executor_from_settings(settings, transport=transport)
    assert ex.max_response_bytes == DEFAULT_MAX_RESPONSE_BYTES
    result = ex.execute_stash({"ok": True}, gateway_authorized=True)
    assert result.outcome is GatewayOutcome.CONTRACT_MISMATCH


def test_story_14_http_timeout_knobs_wire_to_executor() -> None:
    settings = _ready_settings(
        AIBRIDGE_HTTP_TOTAL_TIMEOUT_MS=2500,
        AIBRIDGE_HTTP_CONNECT_TIMEOUT_MS=800,
        AIBRIDGE_GATEWAY_TIMEOUT_SECONDS=99,
    )
    ex = default_executor_from_settings(settings)
    assert ex.timeout_seconds == 2.5
    assert ex.connect_timeout_seconds == 0.8
    assert settings.aibridge_http_connect_timeout_ms == 800


def test_story_14_dockerfile_exists_and_documents_uvicorn() -> None:
    root = Path(__file__).resolve().parents[1]
    dockerfile = root / "Dockerfile"
    assert dockerfile.is_file()
    text = dockerfile.read_text(encoding="utf-8")
    assert "uvicorn" in text
    assert "aibridge.app:app" in text
    assert "python:3.11" in text
