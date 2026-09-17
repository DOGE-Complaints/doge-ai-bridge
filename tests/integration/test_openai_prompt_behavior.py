"""STORY-AIBRIDGE-27 — OAI-001…016 OpenAI / prompt behavior (no live Telegram).

Fixture-driven RecordingResponsesClient / ProductionResponsesClient stubs.
Characterization: OAI-008/009/016 — capture-first; no silent product invent.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from aibridge.app import create_app
from aibridge.audit import get_audit_buffer, reset_audit_buffer
from aibridge.budgets import BudgetGuard, BudgetLimits
from aibridge.config import Settings, reset_settings_cache
from aibridge.confirm import ConfirmationGuard, reset_confirmation_guard
from aibridge.dedupe import EventDedupeStore
from aibridge.gateway import GatewayExecutor, RecordingGatewayTransport
from aibridge.interview import InterviewEngine
from aibridge.readiness import evaluate_readiness
from aibridge.request_assembly import build_stable_prefix
from aibridge.responses_client import (
    DualInstructionsError,
    ProductionResponsesClient,
    RecordingResponsesClient,
    RecordingResponsesTransport,
    ResponsesOutcome,
    ResponsesTransportError,
    assert_prompt_xor,
    assemble_responses_request,
    parse_responses_payload,
)

_TESTS_ROOT = Path(__file__).resolve().parents[1]
if str(_TESTS_ROOT) not in sys.path:
    sys.path.insert(0, str(_TESTS_ROOT))
from fixture_loader import load_fixture  # noqa: E402
from story13_e2e_helpers import (  # noqa: E402
    CHANNEL_TOKEN,
    GATEWAY_TOKEN,
    validation_context,
)

STORY = "STORY-AIBRIDGE-27-qa-openai-prompt-behavior"
OAI_IDS = {f"OAI-{i:03d}" for i in range(1, 17)}
PKG_FIXTURES = (
    _TESTS_ROOT.parents[0]
    / "docs"
    / "tasks"
    / "backlog-stories"
    / "qa-inbound-outbound-data-flow"
    / "fixtures"
)
FORBID = ("Bearer ", "sk-", "callback_data_raw")
SECRET_PROBE = "channel-token-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"


class _RaiseClient(RecordingResponsesClient):
    """Recording client that raises after recording the request."""

    def __init__(self, exc: BaseException) -> None:
        super().__init__(scripted=[])
        self._exc = exc

    def create(self, request: Any) -> dict[str, Any]:
        assert request.payload.get("store") is False
        self.calls.append(dict(request.payload))
        raise self._exc


def _settings(**overrides: object) -> Settings:
    reset_settings_cache()
    base: dict[str, object] = dict(
        AIBRIDGE_CHANNEL_BEARER_TOKEN=CHANNEL_TOKEN,
        DOGESTONIA_API_BEARER_TOKEN=GATEWAY_TOKEN,
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
    return {"Authorization": f"Bearer {CHANNEL_TOKEN}"}


def _build(
    *,
    openai: RecordingResponsesClient | None = None,
    budgets: BudgetGuard | None = None,
    instructions: str = "civic interview",
    pack_id: str = "uus_veerenni_civic/v3",
) -> tuple[TestClient, Any, RecordingResponsesClient, RecordingGatewayTransport, EventDedupeStore]:
    reset_confirmation_guard()
    reset_audit_buffer()
    openai = openai or RecordingResponsesClient(
        scripted=[load_fixture("openai", "text-only-ru-clarify")["payload"]["body"]]
    )
    engine = InterviewEngine(
        client=openai,
        instructions=instructions,
        pack_id=pack_id,
        budgets=budgets,
    )
    store = EventDedupeStore()
    app = create_app(
        settings=_settings(),
        dedupe_store=store,
        interview_engine=engine,
    )
    transport = RecordingGatewayTransport(scripted=[])
    guard: ConfirmationGuard = app.state.confirmation_guard
    guard.executor = GatewayExecutor(
        origin="https://gateway.example.invalid",
        gateway_bearer=GATEWAY_TOKEN,
        channel_bearer=CHANNEL_TOKEN,
        dry_run=True,
        transport=transport,
        redirect_base="https://spa.example.invalid",
    )
    guard.validation_context = validation_context()
    guard.interview_engine = engine
    app.state.interview_engine = engine
    return TestClient(app), app, openai, transport, store


def _body(cluster: str, name: str) -> dict[str, Any]:
    return load_fixture(cluster, name)["payload"]["body"]


def _assert_forbid(text: str) -> None:
    for pat in FORBID:
        assert pat not in text
    assert CHANNEL_TOKEN not in text
    assert GATEWAY_TOKEN not in text
    assert "sk-SHOULD-NOT-LEAK" not in text


def _hash_eq(name: str, cluster: str = "openai") -> None:
    pkg = PKG_FIXTURES / name
    tst = _TESTS_ROOT / "fixtures" / cluster / name
    assert pkg.is_file() and tst.is_file()
    assert pkg.read_bytes() == tst.read_bytes()
    assert hashlib.sha256(pkg.read_bytes()).hexdigest() == hashlib.sha256(
        tst.read_bytes()
    ).hexdigest()


# --- coverage / promote integrity ---


def test_oai_matrix_ids_bound_and_fixtures_present() -> None:
    covered: set[str] = set()
    for cluster in ("openai", "channel"):
        root = _TESTS_ROOT / "fixtures" / cluster
        for path in sorted(root.glob("oai-*.json")) + sorted(root.glob("turns-oai-*.json")) + sorted(
            root.glob("text-only-ru-clarify.json")
        ):
            data = json.loads(path.read_text(encoding="utf-8"))
            for mid in data.get("matrix_ids") or []:
                if str(mid).startswith("OAI-"):
                    covered.add(str(mid))
            assert STORY in (data.get("story_keys") or []) or path.name == "text-only-ru-clarify.json"
    assert OAI_IDS <= covered, f"missing {OAI_IDS - covered}"
    _hash_eq("text-only-ru-clarify.json")
    _hash_eq("oai-empty-output.json")
    _hash_eq("turns-oai-ordinary.json", cluster="channel")


# --- OAI-001…004 happy / fallback ---


def test_oai_001_ordinary_text_interpretation_actions() -> None:
    client, _app, openai, gw, _store = _build(
        openai=RecordingResponsesClient(
            scripted=[load_fixture("openai", "text-only-ru-clarify")["payload"]["body"]]
        )
    )
    r = client.post("/v1/channel/turns", headers=_auth(), json=_body("channel", "turns-oai-ordinary"))
    assert r.status_code == 200
    body = r.json()
    assert "Уточните" in body["reply_text"] or "улиц" in body["reply_text"]
    assert "Received:" not in body["reply_text"]
    assert isinstance(body.get("actions"), list) and len(body["actions"]) >= 1
    # G-02: interpretation labels/styles from offer_interpretation_confirm
    labels = {str(a.get("label") or "") for a in body["actions"]}
    styles = {str(a.get("style") or "") for a in body["actions"]}
    assert {"Looks right", "Edit", "Cancel"} <= labels
    assert {"success", "default", "danger"} <= styles
    assert len(openai.calls) == 1
    assert openai.calls[0]["store"] is False
    assert openai.calls[0]["parallel_tool_calls"] is False
    assert "instructions" not in openai.calls[0]
    assert gw.calls == []
    _assert_forbid(json.dumps(body, ensure_ascii=False))


def test_oai_002_empty_output_fallback() -> None:
    scripted = [load_fixture("openai", "oai-empty-output")["payload"]["body"]]
    engine = InterviewEngine(client=RecordingResponsesClient(scripted=scripted))
    out = engine.run_turn(session_id="s-empty", user_text="hi")
    assert out["ok"] is True
    assert out["reply_text"] == "Acknowledged."
    assert out["gateway_called"] is False


def test_oai_003_received_stub_mapped_to_acknowledged() -> None:
    client, _app, openai, gw, _store = _build(
        openai=RecordingResponsesClient(
            scripted=[load_fixture("openai", "oai-received-stub")["payload"]["body"]]
        )
    )
    r = client.post("/v1/channel/turns", headers=_auth(), json=_body("channel", "turns-oai-ordinary"))
    assert r.status_code == 200
    assert r.json()["reply_text"] == "Acknowledged."
    assert "Received:" not in r.json()["reply_text"]
    assert gw.calls == []
    assert len(openai.calls) == 1


def test_oai_004_cached_token_usage_recorded() -> None:
    scripted = [load_fixture("openai", "oai-cached-tokens")["payload"]["body"]]
    engine = InterviewEngine(
        client=RecordingResponsesClient(scripted=scripted),
        pack_id="uus_veerenni_civic/v3",
    )
    out = engine.run_turn(session_id="s-cache", user_text="hi")
    assert out["ok"] is True
    assert out["cached_input_tokens"] == 150
    events = [e for e in engine.cache.events if e.get("cached_tokens")]
    assert events and events[-1]["cached_tokens"] == 150


# --- OAI-005…007 knobs ---


def test_oai_005_store_true_fails_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    stub = load_fixture("openai", "oai-settings-store-true")["payload"]
    reset_settings_cache()
    monkeypatch.setenv("OPENAI_STORE_RESPONSES", str(stub["OPENAI_STORE_RESPONSES"]))
    with pytest.raises(ValidationError, match="store:false"):
        Settings()
    reset_settings_cache()
    monkeypatch.delenv("OPENAI_STORE_RESPONSES", raising=False)
    s = _settings(OPENAI_API_KEY="sk-test")
    assert s.responses_store_false_enforced() is True
    ready = evaluate_readiness(s, deployment=None)
    assert ready.reason != "openai_store_not_false"


def test_oai_006_xor_stable_prefix_and_instructions() -> None:
    stub = load_fixture("openai", "oai-xor-both-channels")["payload"]
    with pytest.raises(DualInstructionsError):
        assert_prompt_xor(
            has_stable_prefix=bool(stub["has_stable_prefix"]),
            instructions=str(stub["instructions"]),
        )


def test_oai_007_parallel_tool_calls_must_be_false() -> None:
    stub = load_fixture("openai", "oai-parallel-tool-calls")["payload"]
    req = assemble_responses_request(
        model="gpt-test",
        input_items=[{"type": "message", "role": "user", "content": "x"}],
        max_output_tokens=64,
    )
    assert req.payload["parallel_tool_calls"] is stub["parallel_tool_calls"]
    client = RecordingResponsesClient()
    client.create(req)
    assert client.calls[0]["parallel_tool_calls"] is False


# --- OAI-008…011 errors (008/009 characterization) ---


def test_oai_008_429_bounded_no_secret_characterization() -> None:
    """OAI-008 characterization: transport 429 → rate_limited; ASGI raise → 500 shape."""
    err_fx = load_fixture("openai", "oai-http-429")["payload"]
    transport = RecordingResponsesTransport(
        scripted=[(int(err_fx["status"]), err_fx.get("body"), json.dumps(err_fx.get("body")))]
    )
    prod = ProductionResponsesClient(api_key="sk-SHOULD-NOT-LEAK", transport=transport)
    req = assemble_responses_request(
        model="gpt-test",
        input_items=[{"type": "message", "role": "user", "content": "hi"}],
        max_output_tokens=32,
    )
    with pytest.raises(ResponsesTransportError) as ei:
        prod.create(req)
    assert ei.value.outcome == ResponsesOutcome.RATE_LIMITED.value
    _assert_forbid(str(ei.value))

    # Channel path characterization (current implementation): unhandled → 500 internal_error.
    boom = _RaiseClient(ResponsesTransportError(ResponsesOutcome.RATE_LIMITED.value, "rate"))
    _client, app, _oai, gw, store = _build(openai=boom)
    client = TestClient(app, raise_server_exceptions=False)
    r = client.post(
        "/v1/channel/turns",
        headers=_auth(),
        json=_body("channel", "turns-oai-429"),
    )
    assert r.status_code == 500  # characterization
    body = r.json()
    assert body["error"]["code"] == "internal_error"
    assert body["error"]["retryable"] is True
    _assert_forbid(json.dumps(body))
    assert gw.calls == []
    # claim aborted so retry can run
    assert store.get("telegram", "870000008") is None


def test_oai_009_5xx_bounded_characterization() -> None:
    """OAI-009: transport TRANSIENT_FAILURE + ASGI channel depth (G-01 mirror of 008)."""
    err_fx = load_fixture("openai", "oai-http-503")["payload"]
    transport = RecordingResponsesTransport(
        scripted=[(int(err_fx["status"]), None, "upstream")]
    )
    prod = ProductionResponsesClient(api_key="sk-x", transport=transport)
    req = assemble_responses_request(
        model="gpt-test",
        input_items=[{"type": "message", "role": "user", "content": "hi"}],
        max_output_tokens=32,
    )
    with pytest.raises(ResponsesTransportError) as ei:
        prod.create(req)
    assert ei.value.outcome == ResponsesOutcome.TRANSIENT_FAILURE.value
    # characterization: no automatic retry invent on consequential path here

    # G-01: ASGI channel depth — same bounded shape as OAI-008 (no secret/gw; dedupe abort).
    boom = _RaiseClient(
        ResponsesTransportError(ResponsesOutcome.TRANSIENT_FAILURE.value, "upstream 503")
    )
    _client, app, _oai, gw, store = _build(openai=boom)
    client = TestClient(app, raise_server_exceptions=False)
    r = client.post(
        "/v1/channel/turns",
        headers=_auth(),
        json={
            "channel": "telegram",
            "event_id": "870000009",
            "principal": {"user_id": "270000009", "chat_id": "270000009"},
            "message": {"message_id": "9", "text": "503 probe", "language_code": "en"},
        },
    )
    assert r.status_code == 500  # characterization (current implementation)
    body = r.json()
    assert body["error"]["code"] == "internal_error"
    assert body["error"]["retryable"] is True
    _assert_forbid(json.dumps(body))
    assert gw.calls == []
    assert store.get("telegram", "870000009") is None


def test_oai_010_timeout_internal_error_dedupe_abort() -> None:
    boom = _RaiseClient(ResponsesTransportError(ResponsesOutcome.TIMEOUT.value, "timeout"))
    _client, app, _oai, gw, store = _build(openai=boom)
    client = TestClient(app, raise_server_exceptions=False)
    body = _body("channel", "turns-oai-timeout")
    r = client.post("/v1/channel/turns", headers=_auth(), json=body)
    assert r.status_code == 500
    err = r.json()["error"]
    assert err["code"] == "internal_error"
    assert err["retryable"] is True
    assert store.get("telegram", body["event_id"]) is None
    assert gw.calls == []
    # retry after abort can proceed
    ok_client, _a2, openai, gw2, store2 = _build(
        openai=RecordingResponsesClient(
            scripted=[load_fixture("openai", "text-only-ru-clarify")["payload"]["body"]]
        )
    )
    r2 = ok_client.post("/v1/channel/turns", headers=_auth(), json=body)
    assert r2.status_code == 200
    assert len(openai.calls) == 1
    assert gw2.calls == []
    assert store2.get("telegram", body["event_id"]) is not None


def test_oai_011_invalid_openai_body_bounded() -> None:
    # Non-2xx invalid body → bounded transport error (no gateway).
    transport = RecordingResponsesTransport(scripted=[(400, None, "not-json{{{")])
    prod = ProductionResponsesClient(api_key="sk-x", transport=transport)
    req = assemble_responses_request(
        model="gpt-test",
        input_items=[{"type": "message", "role": "user", "content": "hi"}],
        max_output_tokens=32,
    )
    with pytest.raises(ResponsesTransportError) as ei:
        prod.create(req)
    assert ei.value.outcome == ResponsesOutcome.CLIENT_ERROR.value
    boom = _RaiseClient(RuntimeError("invalid body"))
    _c, app, _o, gw, store = _build(openai=boom)
    client = TestClient(app, raise_server_exceptions=False)
    r = client.post(
        "/v1/channel/turns",
        headers=_auth(),
        json={
            "channel": "telegram",
            "event_id": "870000011",
            "principal": {"user_id": "270000011", "chat_id": "270000011"},
            "message": {"message_id": "11", "text": "bad body", "language_code": "en"},
        },
    )
    assert r.status_code == 500
    assert store.get("telegram", "870000011") is None
    assert gw.calls == []
    _assert_forbid(r.text)


# --- OAI-012…016 ---


def test_oai_012_budget_breach_no_gateway() -> None:
    limits = load_fixture("openai", "oai-budget-breach")["payload"]
    budgets = BudgetGuard(BudgetLimits(max_session_turns=int(limits["max_session_turns"])))
    engine = InterviewEngine(
        client=RecordingResponsesClient(
            scripted=[load_fixture("openai", "text-only-ru-clarify")["payload"]["body"]]
        ),
        budgets=budgets,
    )
    engine.last_confirmed_state["s-budget"] = "interviewing"
    out = engine.run_turn(session_id="s-budget", user_text="hi")
    assert out["ok"] is False
    assert out["error"] == "budget_breach"
    assert out["gateway_called"] is False
    assert out["state"] == "interviewing"
    assert isinstance(engine.client, RecordingResponsesClient)
    assert engine.client.calls == []
    assert engine.gateway_invocations == 0


def test_oai_013_no_secret_or_prompt_disclosure() -> None:
    client, app, openai, gw, _store = _build(
        openai=RecordingResponsesClient(
            scripted=[load_fixture("openai", "oai-prompt-injection-reply")["payload"]["body"]]
        ),
        instructions="SYSTEM_SECRET_PROMPT_DO_NOT_LEAK",
    )
    r = client.post(
        "/v1/channel/turns",
        headers=_auth(),
        json=_body("channel", "turns-oai-prompt-injection"),
    )
    assert r.status_code == 200
    body = r.json()
    blob = json.dumps(body, ensure_ascii=False) + json.dumps(openai.calls, ensure_ascii=False)
    assert SECRET_PROBE not in blob
    assert CHANNEL_TOKEN not in body["reply_text"]
    assert "SYSTEM_SECRET_PROMPT_DO_NOT_LEAK" not in body["reply_text"]
    assert gw.calls == []
    _assert_forbid(get_audit_buffer().dump_text())
    assert "SYSTEM_SECRET_PROMPT_DO_NOT_LEAK" not in body.get("reply_text", "")
    _ = app  # harness wired


def test_oai_014_tool_looking_user_text_not_trusted_fc() -> None:
    client, _app, openai, gw, _store = _build(
        openai=RecordingResponsesClient(
            scripted=[load_fixture("openai", "text-only-ru-clarify")["payload"]["body"]]
        )
    )
    r = client.post(
        "/v1/channel/turns",
        headers=_auth(),
        json=_body("channel", "turns-oai-tool-looking-user"),
    )
    assert r.status_code == 200
    body = r.json()
    # user content treated as text → interview actions, not immediate FC send
    assert body.get("outcome") is None
    assert len(openai.calls) == 1
    user_inputs = [
        x
        for x in openai.calls[0].get("input") or []
        if isinstance(x, dict) and x.get("role") == "user"
    ]
    assert user_inputs
    assert "function_call" in str(user_inputs[0].get("content"))
    assert gw.calls == []


def test_oai_015_stable_prefix_identical_across_sessions() -> None:
    stub = load_fixture("openai", "oai-stable-prefix")["payload"]
    tool_json = json.dumps(stub["tools"], sort_keys=True, separators=(",", ":"))
    p1 = build_stable_prefix(
        instructions=stub["instructions"],
        tool_schema_json=tool_json,
        pack_id=stub["pack_id"],
    )
    p2 = build_stable_prefix(
        instructions=stub["instructions"],
        tool_schema_json=tool_json,
        pack_id=stub["pack_id"],
    )
    assert p1 == p2
    assert hashlib.sha256(p1.encode()).hexdigest() == hashlib.sha256(p2.encode()).hexdigest()
    engine_a = InterviewEngine(
        client=RecordingResponsesClient(
            scripted=[load_fixture("openai", "text-only-ru-clarify")["payload"]["body"]]
        ),
        instructions=stub["instructions"],
        pack_id=stub["pack_id"],
    )
    engine_b = InterviewEngine(
        client=RecordingResponsesClient(
            scripted=[load_fixture("openai", "text-only-ru-clarify")["payload"]["body"]]
        ),
        instructions=stub["instructions"],
        pack_id=stub["pack_id"],
    )
    engine_a.run_turn(session_id="sess-a", user_text="a")
    engine_b.run_turn(session_id="sess-b", user_text="b")
    pref_a = next(
        i["content"]
        for i in engine_a.client.calls[0]["input"]
        if i.get("role") == "system"
    )
    pref_b = next(
        i["content"]
        for i in engine_b.client.calls[0]["input"]
        if i.get("role") == "system"
    )
    assert pref_a == pref_b


def test_oai_016_bundle_change_new_prefix_characterization() -> None:
    """OAI-016 characterization: new pack_id → new prefix; no invent of retention branch."""
    stub = load_fixture("openai", "oai-bundle-change")["payload"]
    tool_json = "[]"
    pa = build_stable_prefix(
        instructions=stub["instructions"],
        tool_schema_json=tool_json,
        pack_id=stub["pack_id_a"],
    )
    pb = build_stable_prefix(
        instructions=stub["instructions"],
        tool_schema_json=tool_json,
        pack_id=stub["pack_id_b"],
    )
    assert pa != pb
    # capture: engines constructed with different packs emit different system prefixes
    ea = InterviewEngine(
        client=RecordingResponsesClient(
            scripted=[load_fixture("openai", "text-only-ru-clarify")["payload"]["body"]]
        ),
        instructions=stub["instructions"],
        pack_id=stub["pack_id_a"],
    )
    eb = InterviewEngine(
        client=RecordingResponsesClient(
            scripted=[load_fixture("openai", "text-only-ru-clarify")["payload"]["body"]]
        ),
        instructions=stub["instructions"],
        pack_id=stub["pack_id_b"],
    )
    ea.run_turn(session_id="new-a", user_text="x")
    eb.run_turn(session_id="new-b", user_text="x")
    sa = next(i["content"] for i in ea.client.calls[0]["input"] if i.get("role") == "system")
    sb = next(i["content"] for i in eb.client.calls[0]["input"] if i.get("role") == "system")
    assert sa != sb


def test_parse_empty_and_received_helpers() -> None:
    empty = parse_responses_payload({"id": "r", "output": [], "usage": {}})
    assert empty.reply_text == "Acknowledged."
    # Received: mapping happens in coordinator for channel path; parse keeps text
    stub = parse_responses_payload(
        load_fixture("openai", "oai-received-stub")["payload"]["body"]
    )
    assert stub.reply_text.startswith("Received:")
