"""STORY-AIBRIDGE-14 P6 audit gaps G-01/G-02/G-03."""

from __future__ import annotations

import concurrent.futures

import pytest
from fastapi.testclient import TestClient

from aibridge.app import create_app
from aibridge.config import Settings, reset_settings_cache
from aibridge.confirm_fsm import SessionState
from aibridge.dedupe import EventDedupeStore
from aibridge.gateway import (
    GatewayOutcome,
    RecordingGatewayTransport,
    default_executor_from_settings,
)
from aibridge.migrate import apply_migrations
from aibridge.pg_runtime import GatewayAttemptStore
from aibridge.readiness import evaluate_readiness
from aibridge.request_assembly import schema_validation_complete
from story13_e2e_helpers import (
    DISPOSABLE_URL,
    action_body,
    build_e2e_harness,
    fc_openai_payload,
    followup_openai_payload,
    ok_201,
    pg_available,
    rebuild_app_same_pg,
    text_openai_payload,
    turn_body,
)

pytestmark_pg = pytest.mark.skipif(
    not pg_available(),
    reason="disposable Postgres (.pgdata-test) not running — ./scripts/start-disposable-pg.sh",
)


def _ready_settings(**overrides: object) -> Settings:
    reset_settings_cache()
    base: dict[str, object] = dict(
        AIBRIDGE_CHANNEL_BEARER_TOKEN="channel-token-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        DOGESTONIA_API_BEARER_TOKEN="gateway-token-bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
        DOGESTONIA_INTAKE_BASE_URL="https://gateway.example.invalid",
        DOGESTONIA_DRAFT_REDIRECT_BASE_URL="https://spa.example.invalid",
        OPENAI_API_KEY="sk-test-not-real",
        OPENAI_MODEL="gpt-test",
        AIBRIDGE_DRY_RUN=True,
    )
    base.update(overrides)
    return Settings(**base)


# --- G-01 PG restart / race ---


@pytest.mark.postgres
@pytestmark_pg
def test_story_14_audit_g01_pg_executing_recover_blocks_resend() -> None:
    h = build_e2e_harness(
        openai_scripted=[
            text_openai_payload("Need confirm"),
            fc_openai_payload(call_id="call_pg14"),
        ],
        gateway_scripted=[ok_201()],
    )
    r0 = h.client.post(
        "/v1/channel/turns",
        json=turn_body(event_id="pg14-unk-0", text="hi"),
        headers=h.auth_header,
    )
    interpret_tok = next(
        a["token"] for a in r0.json()["actions"] if a["style"] == "success"
    )
    h.client.post(
        "/v1/channel/actions",
        json=action_body(event_id="pg14-unk-i", token=interpret_tok),
        headers=h.auth_header,
    )
    r1 = h.client.post(
        "/v1/channel/turns",
        json=turn_body(event_id="pg14-unk-1", text="go"),
        headers=h.auth_header,
    )
    send_tok = next(a["token"] for a in r1.json()["actions"] if a["style"] == "primary")
    sess = h.guard.get_or_create_session(user_id="42", chat_id="-100")
    assert isinstance(h.guard.gateway_attempts, GatewayAttemptStore)
    h.guard.gateway_attempts.create_executing(
        session_id=sess.session_id, revision=sess.revision
    )
    sess.state = SessionState.EXECUTING
    h.guard._persist_session(sess)  # noqa: SLF001

    h2 = rebuild_app_same_pg(h)
    # Boot recover_all_executing_attempts must not auto-POST gateway.
    assert h2.transport.calls == []
    sess2 = h2.guard.get_or_create_session(user_id="42", chat_id="-100")
    assert sess2.state is SessionState.UNKNOWN_OUTCOME
    assert h2.guard.send_blocked_for_revision(sess2) is True
    r_s = h2.client.post(
        "/v1/channel/actions",
        json=action_body(
            event_id="pg14-unk-s", token=send_tok, callback_query_id="cbu14"
        ),
        headers=h2.auth_header,
    )
    assert r_s.status_code in {200, 409}
    assert h2.transport.calls == []


@pytest.mark.postgres
@pytestmark_pg
def test_story_14_audit_g01_pg_pending_confirm_survives_restart() -> None:
    h = build_e2e_harness(
        openai_scripted=[
            text_openai_payload("Need confirm"),
            fc_openai_payload(call_id="call_pend14"),
        ],
        gateway_scripted=[ok_201()],
    )
    r0 = h.client.post(
        "/v1/channel/turns",
        json=turn_body(event_id="pg14-pend-0", text="hi"),
        headers=h.auth_header,
    )
    interpret_tok = next(
        a["token"] for a in r0.json()["actions"] if a["style"] == "success"
    )
    h.client.post(
        "/v1/channel/actions",
        json=action_body(event_id="pg14-pend-i", token=interpret_tok),
        headers=h.auth_header,
    )
    r1 = h.client.post(
        "/v1/channel/turns",
        json=turn_body(event_id="pg14-pend-1", text="go"),
        headers=h.auth_header,
    )
    send_tok = next(a["token"] for a in r1.json()["actions"] if a["style"] == "primary")
    sess = h.guard.get_or_create_session(user_id="42", chat_id="-100")
    assert sess.state is SessionState.AWAITING_SEND_CONFIRM
    pending_call = sess.pending_call_id
    frozen = sess.frozen_tool_intent

    h2 = rebuild_app_same_pg(
        h,
        openai_scripted=[followup_openai_payload()],
        gateway_scripted=[ok_201()],
    )
    sess2 = h2.guard.get_or_create_session(user_id="42", chat_id="-100")
    assert sess2.state is SessionState.AWAITING_SEND_CONFIRM
    assert sess2.pending_call_id == pending_call
    assert sess2.frozen_tool_intent == frozen
    r_s = h2.client.post(
        "/v1/channel/actions",
        json=action_body(
            event_id="pg14-pend-s", token=send_tok, callback_query_id="cbp14"
        ),
        headers=h2.auth_header,
    )
    assert r_s.status_code == 200
    assert r_s.json()["outcome"] == GatewayOutcome.STASHED.value
    assert len(h2.transport.calls) == 1


@pytest.mark.postgres
@pytestmark_pg
def test_story_14_audit_g01_pg_unique_executing_race() -> None:
    apply_migrations(DISPOSABLE_URL)
    from aibridge.db import connect_postgres

    conn = connect_postgres(DISPOSABLE_URL)
    conn.execute("TRUNCATE gateway_attempt CASCADE")
    conn.commit()
    conn.close()

    seed = GatewayAttemptStore(DISPOSABLE_URL)
    seed.create_executing(session_id="race-s", revision=7)
    seed.close()
    errors: list[BaseException] = []

    def _dup() -> None:
        store = GatewayAttemptStore(DISPOSABLE_URL)
        try:
            store.create_executing(session_id="race-s", revision=7)
        except Exception as exc:  # noqa: BLE001
            errors.append(exc)
        finally:
            store.close()

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(lambda _: _dup(), range(4)))
    assert len(errors) == 4
    assert all(isinstance(e, RuntimeError) for e in errors)
    check = GatewayAttemptStore(DISPOSABLE_URL)
    rows = check.list_executing()
    assert len([r for r in rows if r["session_id"] == "race-s"]) == 1
    check.close()


# --- G-02 gateway connect timeout ---


def test_story_14_audit_g02_gateway_connect_timeout_wired() -> None:
    settings = _ready_settings(
        AIBRIDGE_DRY_RUN=False,
        AIBRIDGE_HTTP_CONNECT_TIMEOUT_MS=800,
        AIBRIDGE_HTTP_TOTAL_TIMEOUT_MS=2500,
    )
    transport = RecordingGatewayTransport(scripted=[ok_201(draft_id="d-connect")])
    ex = default_executor_from_settings(settings, transport=transport)
    assert ex.connect_timeout_seconds == 0.8
    assert ex.timeout_seconds == 2.5
    result = ex.execute_stash({"ok": True}, gateway_authorized=True)
    assert result.outcome is GatewayOutcome.STASHED
    assert transport.calls
    assert transport.calls[0]["connect_timeout"] == 0.8
    assert transport.calls[0]["timeout"] == 2.5


# --- G-03 schema_validation_complete probe ---


def test_story_14_audit_g03_schema_complete_is_probe_not_tautology() -> None:
    assert schema_validation_complete() is True
    settings = _ready_settings(
        AIBRIDGE_DRY_RUN=False,
        AIBRIDGE_SCHEMA_VALIDATION_COMPLETE=True,
    )
    assert evaluate_readiness(settings).ready is True
    client = TestClient(
        create_app(settings=settings, dedupe_store=EventDedupeStore())
    )
    assert client.get("/readyz").status_code == 200
