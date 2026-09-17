"""STORY-AIBRIDGE-30 — GW-001…020 gateway outcome / continuation (integration).

Fixture-driven RecordingGatewayTransport + GatewayExecutor + ConfirmationGuard.
No live Telegram. Guide must-rows → automated asserts; characterization capture-first.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any
from urllib.parse import quote

import pytest
from fastapi.testclient import TestClient

from aibridge.app import create_app
from aibridge.config import Settings, reset_settings_cache
from aibridge.confirm import ConfirmationGuard
from aibridge.confirm_fsm import IllegalTransitionError, SessionState
from aibridge.dedupe import EventDedupeStore
from aibridge.gateway import (
    GatewayExecutor,
    GatewayOutcome,
    RawHttpResponse,
    RecordingGatewayTransport,
    build_continuation_url,
)
from aibridge.interview import default_recording_engine
from aibridge.pg_runtime import GatewayAttemptStore

_TESTS_ROOT = Path(__file__).resolve().parents[1]
if str(_TESTS_ROOT) not in sys.path:
    sys.path.insert(0, str(_TESTS_ROOT))
from fixture_loader import load_fixture  # noqa: E402

STORY = "STORY-AIBRIDGE-30-qa-gateway-continuation"
GW_IDS = {f"GW-{i:03d}" for i in range(1, 21)}
PKG_FIXTURES = (
    _TESTS_ROOT.parents[0]
    / "docs"
    / "tasks"
    / "backlog-stories"
    / "qa-inbound-outbound-data-flow"
    / "fixtures"
)

GATEWAY_NAMES = [
    "stashed-201",
    "gw-201-missing-trace",
    "gw-201-missing-draft",
    "gw-201-invalid-json",
    "gw-400",
    "gw-401",
    "gw-422",
    "gw-429",
    "gw-503",
    "gw-204",
    "gw-409",
    "gw-redirect",
    "gw-oversized",
]
SPIES_NAMES = [
    "gw-dry-run-ok",
    "gw-stashed-expect",
    "gw-timeout-unknown",
    "gw-looks-right-zero-gw",
    "gw-edit-cancel-zero-gw",
    "gw-restart-executing",
    "gw-fc-followup-fail-stash-auth",
]
SETTINGS_NAMES = [
    "gw-non-https-origin",
    "gw-channel-equals-gateway",
]

GW_BEARER = "gw-story-30-bbbbbbbbbbbbbbbbbbbbbbbbbbbb"
CH_BEARER = "ch-story-30-aaaaaaaaaaaaaaaaaaaaaaaaaaaa"


def _hash(path: Path) -> bytes:
    return hashlib.sha256(path.read_bytes()).digest()


def _raw_from_gateway(name: str) -> RawHttpResponse:
    p = load_fixture("gateway", name)["payload"]
    body = p["body"]
    if isinstance(body, (bytes, bytearray)):
        body_bytes = bytes(body)
    elif isinstance(body, str):
        body_bytes = body.encode("utf-8")
    else:
        body_bytes = json.dumps(body, separators=(",", ":")).encode("utf-8")
    return RawHttpResponse(
        status_code=int(p["status_code"]),
        body=body_bytes,
        final_url=str(p.get("final_url") or ""),
    )


def _executor(
    *,
    scripted: list[RawHttpResponse] | None = None,
    dry_run: bool = False,
    origin: str = "https://gateway.example.invalid",
    raise_on_call: Exception | None = None,
    max_response_bytes: int | None = None,
    redirect_base: str = "https://spa.example.invalid",
) -> tuple[GatewayExecutor, RecordingGatewayTransport]:
    transport = RecordingGatewayTransport(scripted=list(scripted or []))
    if raise_on_call is not None:
        transport.raise_on_call = raise_on_call
    ex = GatewayExecutor(
        origin=origin,
        gateway_bearer=GW_BEARER,
        channel_bearer=CH_BEARER,
        dry_run=dry_run,
        redirect_base=redirect_base,
        transport=transport,
        max_response_bytes=max_response_bytes,
    )
    return ex, transport


def _guard(
    *,
    scripted: list[RawHttpResponse] | None = None,
    dry_run: bool = False,
    raise_on_call: Exception | None = None,
    interview_engine: Any | None = None,
    gateway_attempts: Any | None = None,
) -> tuple[ConfirmationGuard, RecordingGatewayTransport]:
    ex, transport = _executor(
        scripted=scripted, dry_run=dry_run, raise_on_call=raise_on_call
    )
    return (
        ConfirmationGuard(
            executor=ex,
            interview_engine=interview_engine,
            gateway_attempts=gateway_attempts,
        ),
        transport,
    )


def _send_flow(
    g: ConfirmationGuard,
    *,
    user_id: str = "1",
    chat_id: str = "30",
    pending_call_id: str | None = None,
) -> dict[str, Any]:
    sess = g.get_or_create_session(user_id=user_id, chat_id=chat_id)
    interpret = g.offer_interpretation_confirm(sess.session_id)
    g.consume_action_token(
        next(a["token"] for a in interpret if a["style"] == "success"),
        user_id=user_id,
        chat_id=chat_id,
    )
    g.set_frozen_tool_intent(
        sess.session_id, {"title": "pothole", "description": "gw-30"}
    )
    if pending_call_id is not None:
        sess.pending_call_id = pending_call_id
    send_actions = g.offer_send_confirm(sess.session_id)
    send_tok = next(a["token"] for a in send_actions if a["style"] == "primary")
    return g.consume_action_token(send_tok, user_id=user_id, chat_id=chat_id)


def _assert_no_channel_bearer(transport: RecordingGatewayTransport) -> None:
    for call in transport.calls:
        auth = call["headers"].get("Authorization", "")
        assert auth == f"Bearer {GW_BEARER}"
        assert CH_BEARER not in auth
        assert CH_BEARER not in json.dumps(call)


def _settings(**overrides: object) -> Settings:
    reset_settings_cache()
    base: dict[str, object] = dict(
        AIBRIDGE_CHANNEL_BEARER_TOKEN=CH_BEARER,
        DOGESTONIA_API_BEARER_TOKEN=GW_BEARER,
        DATABASE_URL="memory",
        DOGESTONIA_INTAKE_BASE_URL="https://gateway.example.invalid",
        DOGESTONIA_DRAFT_REDIRECT_BASE_URL="https://spa.example.invalid",
        OPENAI_API_KEY="sk-test-not-real",
        OPENAI_MODEL="gpt-test",
        AIBRIDGE_DRY_RUN=True,
    )
    base.update(overrides)
    return Settings(_env_file=None, **base)


def test_fixtures_promoted_hash_eq_and_matrix_coverage() -> None:
    seen: set[str] = set()
    for cluster, names in (
        ("gateway", GATEWAY_NAMES),
        ("spies", SPIES_NAMES),
        ("settings", SETTINGS_NAMES),
    ):
        for name in names:
            env = load_fixture(cluster, name)
            assert env["schema_version"] == "1.0"
            assert STORY in env["story_keys"]
            seen.update(env["matrix_ids"])
            pkg = PKG_FIXTURES / f"{name}.json"
            copy = _TESTS_ROOT / "fixtures" / cluster / f"{name}.json"
            assert pkg.is_file() and copy.is_file()
            assert _hash(pkg) == _hash(copy)
    assert GW_IDS.issubset(seen)


def test_gw_001_dry_run_no_http() -> None:
    spy = load_fixture("spies", "gw-dry-run-ok")["payload"]
    g, transport = _guard(dry_run=True, scripted=[_raw_from_gateway("stashed-201")])
    result = _send_flow(g, chat_id="30-001")
    assert result["ok"] is True
    assert result["outcome"] == spy["outcome"]
    assert result["gateway_invocations"] == spy["gateway_call_count"]
    assert transport.calls == []
    assert result["continuation_url"] is spy["continuation_url"]
    text = (result.get("reply_text") or "").lower()
    for needle in spy["forbid_substrings"]:
        assert needle not in text


def test_gw_002_valid_201_stashed_continuation_url_encoded() -> None:
    seed = load_fixture("gateway", "stashed-201")
    spy = load_fixture("spies", "gw-stashed-expect")["payload"]
    assert "GW-002" in seed["matrix_ids"]
    g, transport = _guard(scripted=[_raw_from_gateway("stashed-201")])
    result = _send_flow(g, chat_id="30-002")
    assert result["ok"] is True
    assert result["outcome"] == spy["outcome"]
    assert result["state"] == spy["state"]
    assert result["draft_id"] == spy["draft_id"]
    assert result["gateway_invocations"] == spy["gateway_call_count"]
    expected = build_continuation_url(
        redirect_base=spy["redirect_base"], draft_id=spy["draft_id"]
    )
    assert result["continuation_url"] == expected
    assert quote(spy["draft_id"], safe="") in (result["continuation_url"] or "")
    assert "Story published" not in (result.get("reply_text") or "")
    assert "not a published" in (result.get("reply_text") or "").lower()
    _assert_no_channel_bearer(transport)
    assert transport.calls[0]["allow_redirects"] is False


@pytest.mark.parametrize(
    ("fixture_name", "matrix_id"),
    [
        ("gw-201-missing-trace", "GW-003"),
        ("gw-201-missing-draft", "GW-004"),
        ("gw-201-invalid-json", "GW-005"),
    ],
)
def test_gw_003_005_contract_mismatch_201(fixture_name: str, matrix_id: str) -> None:
    env = load_fixture("gateway", fixture_name)
    assert matrix_id in env["matrix_ids"]
    ex, transport = _executor(scripted=[_raw_from_gateway(fixture_name)])
    result = ex.execute_stash({"title": "x"}, gateway_authorized=True)
    assert result.outcome is GatewayOutcome.CONTRACT_MISMATCH
    assert result.draft_id is None
    assert result.continuation_url is None
    assert result.http_posted is True
    _assert_no_channel_bearer(transport)


@pytest.mark.parametrize(
    ("fixture_name", "matrix_id", "expected"),
    [
        ("gw-400", "GW-006", GatewayOutcome.VALIDATION_ERROR),
        ("gw-401", "GW-007", GatewayOutcome.GATEWAY_UNAUTHORIZED),
        ("gw-422", "GW-008", GatewayOutcome.GEO_SCOPE_MISMATCH),
        ("gw-429", "GW-009", GatewayOutcome.TRANSIENT_FAILURE),
        ("gw-503", "GW-010", GatewayOutcome.TRANSIENT_FAILURE),
    ],
)
def test_gw_006_010_status_mapping(
    fixture_name: str, matrix_id: str, expected: GatewayOutcome
) -> None:
    env = load_fixture("gateway", fixture_name)
    assert matrix_id in env["matrix_ids"]
    ex, transport = _executor(scripted=[_raw_from_gateway(fixture_name)])
    result = ex.execute_stash({"title": "x"}, gateway_authorized=True)
    assert result.outcome is expected
    assert result.http_posted is True
    blob = result.reply_text + json.dumps(result.__dict__, default=str)
    assert GW_BEARER not in blob
    assert CH_BEARER not in blob
    _assert_no_channel_bearer(transport)


def test_gw_011_timeout_unknown_blocks_resend() -> None:
    spy = load_fixture("spies", "gw-timeout-unknown")["payload"]
    g, transport = _guard(raise_on_call=TimeoutError("read timeout"))
    result = _send_flow(g, chat_id="30-011")
    assert result["ok"] is True
    assert result["outcome"] == spy["outcome"]
    assert result["state"] == spy["state"]
    assert len(transport.calls) == spy["gateway_call_count"]
    sess = g.get_session(result["session_id"])
    assert sess is not None
    assert spy["http_posted"] is True
    assert spy["send_blocked_same_revision"] is True
    assert g.send_blocked_for_revision(sess) is spy["send_blocked_same_revision"]
    # Second Send for same revision must not auto-resend (offer blocked).
    with pytest.raises(IllegalTransitionError):
        sess.state = SessionState.INTERPRETATION_CONFIRMED
        g.set_frozen_tool_intent(sess.session_id, {"title": "retry"})
        g.offer_send_confirm(sess.session_id)
    assert len(transport.calls) == spy["gateway_call_count"]


def test_gw_011_disconnect_ambiguous_unknown_characterization() -> None:
    """Optional GW-011: non-Timeout disconnect → unknown_outcome + http_posted."""
    spy = load_fixture("spies", "gw-timeout-unknown")["payload"]
    ex, transport = _executor(raise_on_call=ConnectionError("peer disconnect"))
    result = ex.execute_stash({"title": "x"}, gateway_authorized=True)
    assert result.outcome is GatewayOutcome.UNKNOWN_OUTCOME
    assert result.http_posted is spy["http_posted"]
    assert len(transport.calls) == 1
    _assert_no_channel_bearer(transport)


@pytest.mark.parametrize(
    ("fixture_name", "matrix_id"),
    [("gw-204", "GW-012"), ("gw-409", "GW-012")],
)
def test_gw_012_unusual_status_unknown_characterization(
    fixture_name: str, matrix_id: str
) -> None:
    """Characterization: current map_http_outcome → unknown_outcome for 204/409."""
    env = load_fixture("gateway", fixture_name)
    assert matrix_id in env["matrix_ids"]
    assert "characterization" in env["notes"]
    ex, transport = _executor(scripted=[_raw_from_gateway(fixture_name)])
    result = ex.execute_stash({"title": "x"}, gateway_authorized=True)
    assert result.outcome is GatewayOutcome.UNKNOWN_OUTCOME
    _assert_no_channel_bearer(transport)


def test_gw_013_redirect_final_url_contract_mismatch() -> None:
    env = load_fixture("gateway", "gw-redirect")
    assert "GW-013" in env["matrix_ids"]
    raw = _raw_from_gateway("gw-redirect")
    ex, transport = _executor(scripted=[raw])
    result = ex.execute_stash({"title": "x"}, gateway_authorized=True)
    assert result.outcome is GatewayOutcome.CONTRACT_MISMATCH
    assert transport.calls[0]["allow_redirects"] is False
    assert raw.final_url != ex.constrained_stash_url()


def test_gw_014_oversized_response_contract_mismatch() -> None:
    env = load_fixture("gateway", "gw-oversized")
    assert "GW-014" in env["matrix_ids"]
    p = env["payload"]
    ex, transport = _executor(
        scripted=[_raw_from_gateway("gw-oversized")],
        max_response_bytes=int(p["max_response_bytes"]),
    )
    result = ex.execute_stash({"title": "x"}, gateway_authorized=True)
    assert result.outcome is GatewayOutcome.CONTRACT_MISMATCH
    assert result.http_posted is True
    _assert_no_channel_bearer(transport)


def test_gw_015_non_https_fail_closed() -> None:
    env = load_fixture("settings", "gw-non-https-origin")
    assert "GW-015" in env["matrix_ids"]
    p = env["payload"]
    settings = _settings(**p["overrides"])
    client = TestClient(
        create_app(
            settings=settings,
            dedupe_store=EventDedupeStore(),
            interview_engine=default_recording_engine(),
        )
    )
    response = client.get("/readyz")
    expect = p["expect_readyz"]
    assert response.status_code == expect["http_status"]
    assert response.json()["reason"] == expect["reason"]

    ex, transport = _executor(origin=p["executor_origin"], scripted=[_raw_from_gateway("stashed-201")])
    result = ex.execute_stash({"title": "x"}, gateway_authorized=True)
    assert result.outcome.value == p["executor_expect_outcome"]
    assert result.http_posted is p["executor_http_posted"]
    assert transport.calls == []


def test_gw_016_equal_bearers_readiness_fails() -> None:
    env = load_fixture("settings", "gw-channel-equals-gateway")
    assert "GW-016" in env["matrix_ids"]
    p = env["payload"]
    settings = _settings(**p["overrides"])
    assert settings.channel_gateway_bearers_equal()
    client = TestClient(
        create_app(
            settings=settings,
            dedupe_store=EventDedupeStore(),
            interview_engine=default_recording_engine(),
        )
    )
    response = client.get("/readyz")
    expect = p["expect_readyz"]
    assert response.status_code == expect["http_status"]
    assert response.json()["reason"] == expect["reason"]


def test_gw_017_interpretation_confirm_zero_gateway() -> None:
    spy = load_fixture("spies", "gw-looks-right-zero-gw")["payload"]
    g, transport = _guard(scripted=[_raw_from_gateway("stashed-201")])
    sess = g.get_or_create_session(user_id="1", chat_id="30-017")
    acts = g.offer_interpretation_confirm(sess.session_id)
    tok = next(a["token"] for a in acts if a["style"] == "success")
    r = g.consume_action_token(tok, user_id="1", chat_id="30-017")
    assert r["ok"] is True
    assert r["http_status"] == spy["http_status"]
    assert r["state"] == spy["state"]
    assert r["gateway_invocations"] == spy["gateway_call_count"]
    assert transport.calls == []


def test_gw_018_edit_cancel_zero_gateway() -> None:
    spy = load_fixture("spies", "gw-edit-cancel-zero-gw")["payload"]
    g, transport = _guard(scripted=[_raw_from_gateway("stashed-201")])
    sess = g.get_or_create_session(user_id="1", chat_id="30-018-edit")
    acts = g.offer_interpretation_confirm(sess.session_id)
    edit_tok = next(a["token"] for a in acts if a["style"] == "default")
    r_edit = g.consume_action_token(edit_tok, user_id="1", chat_id="30-018-edit")
    assert r_edit["ok"] is True
    assert r_edit["state"] == spy["edit_state"]
    assert transport.calls == []

    sess2 = g.get_or_create_session(user_id="1", chat_id="30-018-cancel")
    acts2 = g.offer_interpretation_confirm(sess2.session_id)
    cancel_tok = next(a["token"] for a in acts2 if a["style"] == "danger")
    r_cancel = g.consume_action_token(cancel_tok, user_id="1", chat_id="30-018-cancel")
    assert r_cancel["ok"] is True
    assert r_cancel["state"] == spy["cancel_state"]
    assert r_cancel.get("outcome") == spy["cancel_outcome"]
    assert len(transport.calls) == spy["gateway_call_count"]


class _FakeGwAttemptConn:
    """Minimal conn for GatewayAttemptStore create/list/set/get without live PG."""

    def __init__(self) -> None:
        self._rows: dict[tuple[str, int], dict[str, Any]] = {}
        self._last: dict[str, Any] | None = None
        self._last_many: list[dict[str, Any]] = []

    def execute(self, sql: str, params: tuple[Any, ...] | None = None) -> _FakeGwAttemptConn:
        sql_l = " ".join(sql.lower().split())
        if "insert into gateway_attempt" in sql_l and params is not None:
            key = (str(params[0]), int(params[1]))
            self._rows[key] = {
                "session_id": params[0],
                "revision": int(params[1]),
                "status": "executing",
                "outcome": None,
                "created_at": params[2],
                "updated_at": params[3],
            }
            self._last = None
        elif "update gateway_attempt" in sql_l and params is not None:
            key = (str(params[3]), int(params[4]))
            row = self._rows.get(key)
            if row is not None:
                row["status"] = params[0]
                row["outcome"] = params[1]
                row["updated_at"] = params[2]
            self._last = None
        elif (
            "select * from gateway_attempt" in sql_l
            and "where session_id" in sql_l
            and params is not None
        ):
            self._last = self._rows.get((str(params[0]), int(params[1])))
        elif "status = 'executing'" in sql_l or 'status = "executing"' in sql_l:
            self._last_many = [
                dict(r) for r in self._rows.values() if r.get("status") == "executing"
            ]
            self._last = None
        return self

    def fetchone(self) -> dict[str, Any] | None:
        return self._last

    def fetchall(self) -> list[dict[str, Any]]:
        return list(self._last_many)

    def commit(self) -> None:
        return None

    def rollback(self) -> None:
        return None

    def close(self) -> None:
        return None


def test_gw_019_restart_executing_unknown_no_resend() -> None:
    """G-01: GatewayAttemptStore (fake PG seam) + recover → unknown; no auto-resend."""
    spy = load_fixture("spies", "gw-restart-executing")["payload"]
    fake = _FakeGwAttemptConn()
    store = GatewayAttemptStore("postgresql://fake/aibridge_test", conn=fake)
    g, transport = _guard(
        scripted=[_raw_from_gateway("stashed-201")], gateway_attempts=store
    )
    sess = g.get_or_create_session(user_id="1", chat_id="30-019")
    sid = "s-gw-019-pg"
    sess.session_id = sid
    g._sessions[sess.session_id] = sess  # noqa: SLF001
    sess.state = SessionState.EXECUTING
    sess.revision = 1
    sess.gateway_authorized = True
    store.create_executing(session_id=sid, revision=1)
    assert store.get(session_id=sid, revision=1)["status"] == "executing"
    n = g.recover_all_executing_attempts()
    assert n == 1
    row = store.get(session_id=sid, revision=1)
    assert row is not None
    assert row["status"] == GatewayOutcome.UNKNOWN_OUTCOME.value
    assert sess.state.value == spy["state"]
    assert sess.last_outcome == spy["outcome"]
    assert g.send_blocked_for_revision(sess) is True
    assert len(transport.calls) == spy["gateway_call_count"]
    with pytest.raises(IllegalTransitionError):
        sess.state = SessionState.INTERPRETATION_CONFIRMED
        g.set_frozen_tool_intent(sess.session_id, {"title": "no-resend"})
        g.offer_send_confirm(sess.session_id)
    assert len(transport.calls) == spy["gateway_call_count"]
    store.close()


def test_gw_020_fc_followup_fail_stash_authoritative() -> None:
    spy = load_fixture("spies", "gw-fc-followup-fail-stash-auth")["payload"]

    class _BoomEngine:
        def submit_function_call_output(self, **_kwargs: Any) -> dict[str, Any]:
            raise RuntimeError("openai follow-up failed")

    g, transport = _guard(
        scripted=[_raw_from_gateway("stashed-201")],
        interview_engine=_BoomEngine(),
    )
    result = _send_flow(g, chat_id="30-020", pending_call_id="call_gw_020")
    assert result["ok"] is True
    assert result["outcome"] == spy["outcome"]
    assert result["state"] == spy["state"]
    assert result["draft_id"] == spy["draft_id"]
    assert result["gateway_invocations"] == spy["gateway_call_count"]
    _assert_no_channel_bearer(transport)
