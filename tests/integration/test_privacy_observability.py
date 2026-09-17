"""STORY-AIBRIDGE-32 — SEC-001…010 privacy / logs / observability (integration).

Fixture-driven. Spy bag §14 + Recording* captures. No live Telegram.
No silent product invent — assert existing redaction / store=false / bearer split.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient

from aibridge.action_tokens import ActionTokenStore, TokenActionKind, hash_token
from aibridge.app import create_app
from aibridge.audit import get_audit_buffer, reset_audit_buffer
from aibridge.config import Settings, reset_settings_cache
from aibridge.confirm import ConfirmationGuard, reset_confirmation_guard
from aibridge.dedupe import EventDedupeStore
from aibridge.gateway import GatewayExecutor, RawHttpResponse, RecordingGatewayTransport
from aibridge.interview import InterviewEngine
from aibridge.metrics import assert_no_narrative_in_metrics, reset_metrics
from aibridge.pg_runtime import PostgresActionTokenStore
from aibridge.responses_client import (
    ProductionResponsesClient,
    RecordingResponsesClient,
    RecordingResponsesTransport,
    ResponsesTransportError,
    assemble_responses_request,
    redact_secrets,
)
from aibridge.tool_gen import (
    CANONICAL_OPERATION_ID,
    SERVER_OWNED_FIELD_PATHS,
    generate_strict_tool,
    to_responses_flat_tool,
)

_TESTS_ROOT = Path(__file__).resolve().parents[1]
if str(_TESTS_ROOT) not in sys.path:
    sys.path.insert(0, str(_TESTS_ROOT))
from fixture_loader import load_fixture  # noqa: E402

STORY = "STORY-AIBRIDGE-32-qa-privacy-logs-observability"
SEC_IDS = {f"SEC-{i:03d}" for i in range(1, 11)}
PKG_FIXTURES = (
    _TESTS_ROOT.parents[0]
    / "docs"
    / "tasks"
    / "backlog-stories"
    / "qa-inbound-outbound-data-flow"
    / "fixtures"
)
REPO = _TESTS_ROOT.parents[0]
WIRE_OAS = REPO / "docs" / "openapi" / "story-intake-actions.openapi.yaml"
PACK_SCHEMA = _TESTS_ROOT / "fixtures" / "content" / "pack" / "payload.schema.json"

CHANNEL = "channel-token-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
GATEWAY = "gateway-token-bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"

FIXTURE_NAMES = [
    ("spies", "sec-narrative-absent"),
    ("spies", "sec-secret-redacted"),
    ("spies", "sec-channel-audit-bounded"),
    ("spies", "sec-metrics-scrub"),
    ("spies", "sec-error-envelope"),
    ("spies", "sec-token-hash-only"),
    ("spies", "sec-openai-store-false"),
    ("spies", "sec-gateway-bearer-only"),
    ("spies", "sec-n8n-export-secret-free"),
    ("spies", "sec-prompt-injection-allowlist"),
    ("channel", "sec-turns-pii-narrative"),
]


def _hash(path: Path) -> bytes:
    return hashlib.sha256(path.read_bytes()).digest()


def _settings(**overrides: object) -> Settings:
    reset_settings_cache()
    base: dict[str, object] = dict(
        AIBRIDGE_CHANNEL_BEARER_TOKEN=CHANNEL,
        DOGESTONIA_API_BEARER_TOKEN=GATEWAY,
        DATABASE_URL="memory",
        AIBRIDGE_ALLOW_MEMORY_STORES=True,
        DOGESTONIA_INTAKE_BASE_URL="https://gateway.example.invalid",
        DOGESTONIA_DRAFT_REDIRECT_BASE_URL="https://spa.example.invalid",
        OPENAI_API_KEY="",
        OPENAI_MODEL="gpt-test",
        AIBRIDGE_DRY_RUN=True,
    )
    base.update(overrides)
    return Settings(_env_file=None, **base)


def _auth() -> dict[str, str]:
    return {"Authorization": f"Bearer {CHANNEL}"}


def _build(
    *,
    openai: RecordingResponsesClient | None = None,
    tools: list[dict[str, Any]] | None = None,
    dry_run: bool = True,
    gateway_scripted: list[RawHttpResponse] | None = None,
) -> tuple[TestClient, Any, RecordingResponsesClient, RecordingGatewayTransport]:
    reset_confirmation_guard()
    reset_audit_buffer()
    reset_metrics()
    openai = openai or RecordingResponsesClient(
        scripted=[
            {
                "id": "resp_sec",
                "output": [
                    {
                        "type": "message",
                        "role": "assistant",
                        "content": [{"type": "output_text", "text": "Уточните детали."}],
                    }
                ],
                "usage": {"input_tokens": 1, "output_tokens": 1},
            }
        ]
    )
    engine = InterviewEngine(
        client=openai,
        instructions="civic interview",
        pack_id="uus_veerenni_civic/v3",
        tools=list(tools or []),
    )
    app = create_app(
        settings=_settings(AIBRIDGE_DRY_RUN=dry_run),
        dedupe_store=EventDedupeStore(),
        interview_engine=engine,
    )
    transport = RecordingGatewayTransport(scripted=list(gateway_scripted or []))
    guard: ConfirmationGuard = app.state.confirmation_guard
    guard.executor = GatewayExecutor(
        origin="https://gateway.example.invalid",
        gateway_bearer=GATEWAY,
        channel_bearer=CHANNEL,
        dry_run=dry_run,
        transport=transport,
        redirect_base="https://spa.example.invalid",
    )
    guard.interview_engine = engine
    app.state.interview_engine = engine
    return TestClient(app), app, openai, transport


def _turns_pii() -> dict[str, Any]:
    return load_fixture("channel", "sec-turns-pii-narrative")["payload"]["body"]


def _spy(name: str) -> dict[str, Any]:
    return load_fixture("spies", name)["payload"]


def _hash_eq(name: str, cluster: str) -> None:
    pkg = PKG_FIXTURES / f"{name}.json"
    copy = _TESTS_ROOT / "fixtures" / cluster / f"{name}.json"
    assert pkg.is_file() and copy.is_file()
    assert _hash(pkg) == _hash(copy)


# --- coverage / promote integrity ---


def test_sec_matrix_ids_bound_and_fixtures_hash_eq() -> None:
    covered: set[str] = set()
    for cluster, name in FIXTURE_NAMES:
        env = load_fixture(cluster, name)
        assert env["schema_version"] == "1.0"
        assert STORY in env["story_keys"]
        covered.update(str(m) for m in (env.get("matrix_ids") or []))
        _hash_eq(name, cluster)
    assert SEC_IDS <= covered, f"missing {SEC_IDS - covered}"


# --- SEC-001 ---


def test_sec_001_narrative_absent_from_audit_and_metrics() -> None:
    spy = _spy("sec-narrative-absent")
    client, _app, _openai, _gw = _build()
    r = client.post("/v1/channel/turns", headers=_auth(), json=_turns_pii())
    assert r.status_code == 200
    audit = get_audit_buffer().dump_text()
    metrics = client.get("/metrics").text
    for needle in spy["forbid_in_audit"]:
        assert needle not in audit
    for needle in spy["forbid_in_metrics"]:
        assert needle not in metrics
        assert_no_narrative_in_metrics(metrics, sample=needle)


# --- SEC-002 ---


def test_sec_002_secret_redacted_from_response_and_logs() -> None:
    spy = _spy("sec-secret-redacted")
    secret = spy["secret"]
    # Direct redact helper.
    assert secret not in redact_secrets(f"boom {secret} more", secret)
    # Production client maps errors through redact_secrets(api_key).
    transport = RecordingResponsesTransport(
        scripted=[(500, None, f"upstream failed key={secret}")]
    )
    prod = ProductionResponsesClient(api_key=secret, transport=transport)
    req = assemble_responses_request(
        model="gpt-test",
        input_items=[{"type": "message", "role": "user", "content": "hi"}],
        max_output_tokens=32,
    )
    with pytest.raises(ResponsesTransportError) as ei:
        prod.create(req)
    err_text = str(ei.value)
    for needle in spy["forbid_substrings"]:
        assert needle not in err_text
    # Channel path: raised message with secret must not appear in JSON body.
    class _Boom(RecordingResponsesClient):
        def create(self, request: Any) -> dict[str, Any]:
            self.calls.append(dict(request.payload))
            raise RuntimeError(f"engine failed: {secret}")

    _client, app, _o, _gw = _build(openai=_Boom())
    tc = TestClient(app, raise_server_exceptions=False)
    r = tc.post("/v1/channel/turns", headers=_auth(), json=_turns_pii())
    assert r.status_code == 500
    body_text = r.text
    audit = get_audit_buffer().dump_text()
    for needle in spy["forbid_substrings"]:
        assert needle not in body_text
        assert needle not in audit


# --- SEC-003 ---


def test_sec_003_channel_audit_bounded_no_bearer_or_narrative() -> None:
    spy = _spy("sec-channel-audit-bounded")
    client, _app, _openai, _gw = _build()
    r = client.post("/v1/channel/turns", headers=_auth(), json=_turns_pii())
    assert r.status_code == 200
    audit = get_audit_buffer().dump_text()
    for needle in spy["forbid_in_audit"]:
        assert needle not in audit
    if spy.get("allow_bounded_markers"):
        buf = get_audit_buffer()
        assert isinstance(buf.records, list)
        for rec in buf.records:
            assert "event" in rec
            detail = str(rec.get("detail") or "")
            assert CHANNEL not in detail
            assert "Bearer " not in detail


# --- SEC-004 ---


def test_sec_004_metrics_scrub_counts_only() -> None:
    spy = _spy("sec-metrics-scrub")
    client, _app, _openai, _gw = _build()
    r = client.post("/v1/channel/turns", headers=_auth(), json=_turns_pii())
    assert r.status_code == 200
    metrics = client.get("/metrics")
    assert metrics.status_code == 200
    body = metrics.text
    assert spy["require_metric_prefix"] in body
    for needle in spy["forbid_in_metrics"]:
        assert needle not in body


# --- SEC-005 ---


def test_sec_005_error_envelope_stable_request_id() -> None:
    spy = _spy("sec-error-envelope")
    client, _app, _openai, _gw = _build()
    r = client.post("/v1/channel/turns", json=_turns_pii())  # no auth
    assert r.status_code == spy["http_status"]
    body = r.json()
    assert "request_id" in body and body["request_id"]
    err = body["error"]
    for key in spy["error_keys"]:
        assert key in err
    assert set(err.keys()) >= set(spy["error_keys"])
    # Bounded: no raw tokens in envelope.
    blob = json.dumps(body)
    assert CHANNEL not in blob
    assert GATEWAY not in blob
    assert "Bearer " not in blob


# --- SEC-006 ---


class _FakePgConn:
    """Minimal conn for PostgresActionTokenStore.issue/peek without live PG (G-01)."""

    def __init__(self) -> None:
        self.insert_params: list[tuple[Any, ...]] = []
        self._rows: dict[str, dict[str, Any]] = {}
        self._last: dict[str, Any] | None = None
        self.rowcount = 0

    def execute(self, sql: str, params: tuple[Any, ...] | None = None) -> _FakePgConn:
        sql_l = " ".join(sql.lower().split())
        if "insert into action_token" in sql_l and params is not None:
            self.insert_params.append(params)
            th = str(params[0])
            self._rows[th] = {
                "token_hash": params[0],
                "action": params[1],
                "session_id": params[2],
                "user_id": params[3],
                "chat_id": params[4],
                "deployment_id": params[5],
                "revision": params[6],
                "issued_at": params[7],
                "expires_at": params[8],
                "expected_state": params[9],
                "state": params[10],
                "operation_id": params[11],
                "draft_hash": params[12],
                "nonce": params[13],
            }
            self._last = None
        elif "select * from action_token" in sql_l and params is not None:
            self._last = self._rows.get(str(params[0]))
        return self

    def fetchone(self) -> dict[str, Any] | None:
        return self._last

    def commit(self) -> None:
        return None

    def close(self) -> None:
        return None


def test_sec_006_token_store_hash_only() -> None:
    spy = _spy("sec-token-hash-only")
    store = ActionTokenStore()
    raw, rec = store.issue(
        action=TokenActionKind.CONFIRM_INTERPRETATION,
        session_id="s-sec-006",
        user_id="32",
        chat_id="32",
        deployment_id="local",
        revision=1,
        expected_state="awaiting_interpretation_confirm",
    )
    assert spy["raw_stored"] is False
    keys = list(store._by_hash.keys())  # type: ignore[attr-defined]
    assert raw not in keys
    if spy.get("forbid_substrings_in_store_keys"):
        assert all(raw not in str(k) for k in keys)
    assert hash_token(raw) in store._by_hash  # type: ignore[attr-defined]
    snap = store.bind_snapshot(raw)
    assert snap["raw_stored"] is False
    assert "raw" not in snap
    assert snap["token_hash"] == rec.token_hash
    assert raw not in json.dumps(snap)


def test_sec_006_pg_store_hash_only_no_raw_in_insert() -> None:
    """G-01: PostgresActionTokenStore persists hash only (fake conn Preference A)."""
    spy = _spy("sec-token-hash-only")
    fake = _FakePgConn()
    store = PostgresActionTokenStore(
        "postgresql://fake/aibridge_test",
        conn=fake,
    )
    raw, rec = store.issue(
        action=TokenActionKind.CONFIRM_INTERPRETATION,
        session_id="s-sec-006-pg",
        user_id="32",
        chat_id="32-pg",
        deployment_id="local",
        revision=1,
        expected_state="awaiting_interpretation_confirm",
    )
    assert spy["raw_stored"] is False
    assert spy.get("forbid_substrings_in_store_keys") is True
    assert len(fake.insert_params) == 1
    params = fake.insert_params[0]
    assert raw not in params
    assert all(raw not in str(p) for p in params if p is not None)
    assert params[0] == hash_token(raw) == rec.token_hash
    peeked = store.peek(raw)
    assert peeked.token_hash == rec.token_hash
    row_blob = json.dumps(fake._rows[rec.token_hash], sort_keys=True, default=str)
    assert raw not in row_blob
    store.close()


# --- SEC-007 ---


def test_sec_007_openai_capture_store_false_no_secrets() -> None:
    spy = _spy("sec-openai-store-false")
    client, _app, openai, gw = _build()
    r = client.post("/v1/channel/turns", headers=_auth(), json=_turns_pii())
    assert r.status_code == 200
    assert len(openai.calls) == 1
    capture = openai.calls[0]
    assert capture.get("store") is spy["store"] is False
    blob = json.dumps(capture, ensure_ascii=False)
    for needle in spy["forbid_in_capture"]:
        assert needle not in blob
    assert gw.calls == []


# --- SEC-008 ---


def test_sec_008_gateway_bearer_only_no_channel() -> None:
    spy = _spy("sec-gateway-bearer-only")
    stash = RawHttpResponse(
        status_code=201,
        body=json.dumps({"draft_id": "d-sec-008", "trace_id": "t-sec"}).encode(),
    )
    client, app, _openai, transport = _build(
        dry_run=False, gateway_scripted=[stash]
    )
    guard: ConfirmationGuard = app.state.confirmation_guard
    sess = guard.get_or_create_session(user_id="32", chat_id="32-008")
    interpret = guard.offer_interpretation_confirm(sess.session_id)
    guard.consume_action_token(
        next(a["token"] for a in interpret if a["style"] == "success"),
        user_id="32",
        chat_id="32-008",
    )
    guard.set_frozen_tool_intent(
        sess.session_id,
        {
            "name": CANONICAL_OPERATION_ID,
            "call_id": "call_sec008",
            "arguments": {
                "narrative": {"note": "sec"},
                "schema_binding": {"structured_payload": {"title": "sec"}},
            },
        },
    )
    send_actions = guard.offer_send_confirm(sess.session_id)
    send_tok = next(a["token"] for a in send_actions if a["style"] == "primary")
    result = guard.consume_action_token(send_tok, user_id="32", chat_id="32-008")
    assert result.get("ok") is True or result.get("outcome") in {
        "stashed",
        "dry_run_ok",
    } or "outcome" in result or result.get("state")
    assert len(transport.calls) >= 1
    for call in transport.calls:
        auth = call["headers"].get("Authorization", "")
        assert auth.startswith(spy["gateway_bearer_prefix"])
        assert auth == f"Bearer {GATEWAY}"
        for needle in spy["forbid_authorization_substrings"]:
            assert needle not in auth
        blob = json.dumps(call, ensure_ascii=False)
        assert CHANNEL not in blob
    _ = client  # harness built


# --- SEC-009 ---


def test_sec_009_n8n_export_docs_secret_free() -> None:
    spy = _spy("sec-n8n-export-secret-free")
    blobs: list[str] = []
    for pattern in spy["scan_globs"]:
        # Fixture globs use trailing /** — resolve to directory rglob.
        root_pat = pattern.rstrip("/").removesuffix("/**").removesuffix("**")
        root = REPO / root_pat
        assert root.is_dir(), root
        for path in sorted(root.rglob("*")):
            if path.is_file():
                blobs.append(path.read_text(encoding="utf-8"))
    assert blobs, "n8n ops docs must exist for SEC-009 scan"
    joined = "\n".join(blobs)
    for needle in spy["forbid_substrings"]:
        assert needle not in joined


# --- SEC-010 ---


def test_sec_010_prompt_injection_allowlist_server_owned() -> None:
    """G-02: tool_gen allowlisted surface + channel forbid; no evil tool/URL."""
    spy = _spy("sec-prompt-injection-allowlist")
    channel = load_fixture("channel", "sec-turns-pii-narrative")
    forbid_narrative = channel["payload"]["forbid_narrative_substrings"]
    generated = generate_strict_tool(
        wire_oas_path=WIRE_OAS,
        pack_schema_path=PACK_SCHEMA,
        schema_id="tallinn_civic",
        schema_version="v1",
    )
    tool = to_responses_flat_tool(generated)
    assert tool["name"] == spy["canonical_operation_id"] == CANONICAL_OPERATION_ID
    # Negative: evil tool must never be offered alongside allowlisted surface.
    evil = {
        "type": "function",
        "name": "callEvilUrl",
        "strict": True,
        "parameters": {
            "type": "object",
            "properties": {"url": {"type": "string"}},
            "additionalProperties": False,
            "required": ["url"],
        },
    }
    client, _app, openai, gw = _build(tools=[tool])  # only allowlisted
    body = dict(channel["payload"]["body"])
    body["event_id"] = "sec-evt-010"
    body["message"] = {
        "message_id": "10",
        "text": spy["injection_text"],
    }
    r = client.post("/v1/channel/turns", headers=_auth(), json=body)
    assert r.status_code == 200
    assert len(openai.calls) == 1
    capture = openai.calls[0]
    tools = capture.get("tools") or []
    names = {t.get("name") for t in tools if isinstance(t, dict)}
    assert names == {spy["canonical_operation_id"]}
    assert evil["name"] not in names
    tools_blob = json.dumps(tools, ensure_ascii=False)
    assert "https://evil.example/steal" not in tools_blob
    assert "callEvilUrl" not in tools_blob
    props = (tools[0].get("parameters") or {}).get("properties") or {}
    # Server-owned HTTP/gateway knobs must not be model-writable.
    for leaf in ("Authorization", "authorization", "gateway_url", "gateway_method"):
        assert leaf not in props
        assert leaf in SERVER_OWNED_FIELD_PATHS or leaf.lower() in {
            p.lower() for p in SERVER_OWNED_FIELD_PATHS
        }
    # origin may appear in wire-projected schema; still server-owned (assemble overrides).
    assert "origin" in SERVER_OWNED_FIELD_PATHS
    assert "origin" in spy["server_owned_fields"]
    xa = tools[0].get("x_aibridge") or {}
    assert xa.get("operation_path")  # server metadata from tool_gen, not injection URL
    assert "evil.example" not in str(xa.get("operation_path") or "")
    audit = get_audit_buffer().dump_text()
    metrics = client.get("/metrics").text
    for needle in forbid_narrative:
        assert needle not in audit
        assert needle not in metrics
    blob = json.dumps(capture, ensure_ascii=False)
    assert gw.calls == []
    assert CHANNEL not in blob
    assert GATEWAY not in blob
