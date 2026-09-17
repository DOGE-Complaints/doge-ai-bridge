"""STORY-AIBRIDGE-29 — ACT-001…018 action-token / dual-confirm FSM (unit).

Fixture-driven ConfirmationGuard + ActionTokenStore. No live Telegram.
Guide must-rows → automated asserts; no silent product invent.
"""

from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path
from typing import Any

from aibridge.action_tokens import ActionTokenStore, TokenActionKind, hash_token, mint_opaque_token
from aibridge.confirm import ConfirmationGuard
from aibridge.confirm_fsm import SessionState
from aibridge.gateway import GatewayExecutor, RawHttpResponse, RecordingGatewayTransport
from aibridge.pg_runtime import PostgresActionTokenStore

_TESTS_ROOT = Path(__file__).resolve().parents[1]
if str(_TESTS_ROOT) not in sys.path:
    sys.path.insert(0, str(_TESTS_ROOT))
from fixture_loader import load_fixture  # noqa: E402

STORY = "STORY-AIBRIDGE-29-qa-action-token-fsm"
ACT_IDS = {f"ACT-{i:03d}" for i in range(1, 19)}
PKG_FIXTURES = (
    _TESTS_ROOT.parents[0]
    / "docs"
    / "tasks"
    / "backlog-stories"
    / "qa-inbound-outbound-data-flow"
    / "fixtures"
)

CHANNEL_NAMES = [
    "act-looks-right",
    "act-edit",
    "act-cancel",
    "act-send",
    "act-random-token",
    "act-foreign-user",
    "act-foreign-chat",
    "act-expired",
    "act-consumed-retry",
    "act-invalidated-sibling",
    "act-revision-mismatch",
    "act-expected-state-mismatch",
    "act-deployment-mismatch",
    "act-draft-hash-mismatch",
    "act-frozen-missing",
    "act-illegal-fsm",
    "act-token-len-65",
]
SPIES_NAMES = [
    "act-looks-right-zero-gw",
    "act-edit-no-gw",
    "act-cancel-no-gw",
    "act-send-one-gw",
    "act-reject-404",
    "act-reject-403",
    "act-reject-409",
    "act-hash-only-persist",
    "act-facade-422",
]


def _hash(path: Path) -> bytes:
    return hashlib.sha256(path.read_bytes()).digest()


def _spy(name: str) -> dict[str, Any]:
    return load_fixture("spies", name)["payload"]


def _stash_raw() -> RawHttpResponse:
    return RawHttpResponse(
        status_code=201,
        body=json.dumps(
            {"data": {"draft_id": "draft-act-29"}, "trace_id": "trace-act-29"}
        ).encode(),
    )


def _guard_recording() -> tuple[ConfirmationGuard, RecordingGatewayTransport]:
    transport = RecordingGatewayTransport(scripted=[_stash_raw()])
    executor = GatewayExecutor(
        origin="https://gateway.example.invalid",
        gateway_bearer="gw-act-29",
        channel_bearer="ch-act-29",
        transport=transport,
        redirect_base="https://spa.example.invalid",
    )
    return ConfirmationGuard(executor=executor), transport


def _looks_right_tok(g: ConfirmationGuard, sess_id: str) -> str:
    acts = g.offer_interpretation_confirm(sess_id)
    return next(a["token"] for a in acts if a["style"] == "success")


def _send_tok(g: ConfirmationGuard, sess_id: str, *, draft_hash: str | None = None) -> str:
    g.set_frozen_tool_intent(
        sess_id,
        {"title": "pothole", "description": "act-29"},
        draft_hash=draft_hash,
    )
    acts = g.offer_send_confirm(sess_id)
    return next(a["token"] for a in acts if a["style"] == "primary")


def test_fixtures_promoted_hash_eq_and_matrix_coverage() -> None:
    seen: set[str] = set()
    for cluster, names in (("channel", CHANNEL_NAMES), ("spies", SPIES_NAMES)):
        for name in names:
            env = load_fixture(cluster, name)
            assert env["schema_version"] == "1.0"
            assert STORY in env["story_keys"]
            seen.update(env["matrix_ids"])
            pkg = PKG_FIXTURES / f"{name}.json"
            copy = _TESTS_ROOT / "fixtures" / cluster / f"{name}.json"
            assert pkg.is_file() and copy.is_file()
            assert _hash(pkg) == _hash(copy)
    assert ACT_IDS.issubset(seen)


def test_act_001_looks_right_zero_gateway() -> None:
    spy = _spy("act-looks-right-zero-gw")
    g, transport = _guard_recording()
    sess = g.get_or_create_session(user_id="1", chat_id="29-001")
    tok = _looks_right_tok(g, sess.session_id)
    r = g.consume_action_token(tok, user_id="1", chat_id="29-001")
    assert r["ok"] is True
    assert r["http_status"] == spy["http_status"]
    assert r["state"] == spy["state"]
    assert r["gateway_invocations"] == spy["gateway_call_count"]
    assert transport.calls == []


def test_act_002_edit_revision_invalidates_siblings() -> None:
    spy = _spy("act-edit-no-gw")
    g, transport = _guard_recording()
    sess = g.get_or_create_session(user_id="1", chat_id="29-002")
    acts = g.offer_interpretation_confirm(sess.session_id)
    edit_tok = next(a["token"] for a in acts if a["style"] == "default")
    sibling = next(a["token"] for a in acts if a["style"] == "success")
    old_rev = sess.revision
    r = g.consume_action_token(edit_tok, user_id="1", chat_id="29-002")
    assert r["ok"] is True
    assert r["http_status"] == spy["http_status"]
    assert r["state"] == spy["state"]
    assert sess.revision == old_rev + spy["revision_delta"]
    assert transport.calls == []
    bad = g.consume_action_token(sibling, user_id="1", chat_id="29-002")
    assert bad["http_status"] == 409


def test_act_003_cancel_invalidates_no_gateway() -> None:
    spy = _spy("act-cancel-no-gw")
    g, transport = _guard_recording()
    sess = g.get_or_create_session(user_id="1", chat_id="29-003")
    acts = g.offer_interpretation_confirm(sess.session_id)
    cancel_tok = next(a["token"] for a in acts if a["style"] == "danger")
    sibling = next(a["token"] for a in acts if a["style"] == "success")
    r = g.consume_action_token(cancel_tok, user_id="1", chat_id="29-003")
    assert r["ok"] is True
    assert r["state"] == spy["state"]
    assert r["gateway_invocations"] == spy["gateway_call_count"]
    assert transport.calls == []
    bad = g.consume_action_token(sibling, user_id="1", chat_id="29-003")
    assert bad["http_status"] == 409


def test_act_004_send_one_authorized_frozen_body() -> None:
    spy = _spy("act-send-one-gw")
    g, transport = _guard_recording()
    sess = g.get_or_create_session(user_id="1", chat_id="29-004")
    g.consume_action_token(_looks_right_tok(g, sess.session_id), user_id="1", chat_id="29-004")
    frozen = {"title": "pothole", "description": "act-29-frozen"}
    g.set_frozen_tool_intent(sess.session_id, frozen)
    tok = next(
        a["token"] for a in g.offer_send_confirm(sess.session_id) if a["style"] == "primary"
    )
    r = g.consume_action_token(tok, user_id="1", chat_id="29-004")
    assert r["ok"] is True
    assert r["http_status"] == spy["http_status"]
    assert r["gateway_invocations"] == spy["gateway_call_count"]
    assert len(transport.calls) == 1
    assert transport.calls[0]["json_body"] == frozen


def test_act_005_random_token_404() -> None:
    spy = _spy("act-reject-404")
    g, transport = _guard_recording()
    body = load_fixture("channel", "act-random-token")["payload"]["body"]
    r = g.consume_action_token(
        body["action_token"],
        user_id=body["principal"]["user_id"],
        chat_id=body["principal"]["chat_id"],
    )
    assert r["ok"] is False
    assert r["http_status"] == spy["http_status"]
    assert r["code"] == spy["error_code"]
    assert transport.calls == []


def test_act_006_foreign_user_403() -> None:
    spy = _spy("act-reject-403")
    g, transport = _guard_recording()
    sess = g.get_or_create_session(user_id="1", chat_id="29-006")
    tok = _looks_right_tok(g, sess.session_id)
    r = g.consume_action_token(tok, user_id="999", chat_id="29-006")
    assert r["http_status"] == spy["http_status"]
    assert r["code"] == spy["error_code"]
    assert transport.calls == []


def test_act_007_foreign_chat_403() -> None:
    spy = _spy("act-reject-403")
    g, transport = _guard_recording()
    sess = g.get_or_create_session(user_id="1", chat_id="29-007")
    tok = _looks_right_tok(g, sess.session_id)
    r = g.consume_action_token(tok, user_id="1", chat_id="other-chat")
    assert r["http_status"] == spy["http_status"]
    assert r["code"] == spy["error_code"]
    assert transport.calls == []


def test_act_008_expired_token_409() -> None:
    spy = _spy("act-reject-409")
    g, transport = _guard_recording()
    sess = g.get_or_create_session(user_id="1", chat_id="29-008")
    tok = _looks_right_tok(g, sess.session_id)
    rec = g.tokens.lookup(tok)
    rec.expires_at = time.time() - 1
    r = g.consume_action_token(tok, user_id="1", chat_id="29-008")
    assert r["http_status"] == spy["http_status"]
    assert r["code"] == spy["error_code"]
    assert transport.calls == []


def test_act_009_consumed_token_new_event_409() -> None:
    spy = _spy("act-reject-409")
    g, _transport = _guard_recording()
    sess = g.get_or_create_session(user_id="1", chat_id="29-009")
    tok = _looks_right_tok(g, sess.session_id)
    assert g.consume_action_token(tok, user_id="1", chat_id="29-009")["ok"] is True
    r2 = g.consume_action_token(tok, user_id="1", chat_id="29-009")
    assert r2["http_status"] == spy["http_status"]


def test_act_010_invalidated_sibling_409() -> None:
    spy = _spy("act-reject-409")
    g, transport = _guard_recording()
    sess = g.get_or_create_session(user_id="1", chat_id="29-010")
    acts = g.offer_interpretation_confirm(sess.session_id)
    cancel_tok = next(a["token"] for a in acts if a["style"] == "danger")
    sibling = next(a["token"] for a in acts if a["style"] == "success")
    g.consume_action_token(cancel_tok, user_id="1", chat_id="29-010")
    bad = g.consume_action_token(sibling, user_id="1", chat_id="29-010")
    assert bad["http_status"] == spy["http_status"]
    assert transport.calls == []


def test_act_011_revision_mismatch_409() -> None:
    spy = _spy("act-reject-409")
    g, transport = _guard_recording()
    sess = g.get_or_create_session(user_id="1", chat_id="29-011")
    tok = _looks_right_tok(g, sess.session_id)
    sess.revision += 1
    r = g.consume_action_token(tok, user_id="1", chat_id="29-011")
    assert r["http_status"] == spy["http_status"]
    assert "revision" in r["message"].lower()
    assert transport.calls == []


def test_act_012_expected_state_mismatch_409() -> None:
    spy = _spy("act-reject-409")
    g, transport = _guard_recording()
    sess = g.get_or_create_session(user_id="1", chat_id="29-012")
    tok = _looks_right_tok(g, sess.session_id)
    sess.state = SessionState.INTERPRETATION_CONFIRMED
    r = g.consume_action_token(tok, user_id="1", chat_id="29-012")
    assert r["http_status"] == spy["http_status"]
    assert "state" in r["message"].lower()
    assert transport.calls == []


def test_act_013_deployment_mismatch_409() -> None:
    spy = _spy("act-reject-409")
    g, transport = _guard_recording()
    sess = g.get_or_create_session(user_id="1", chat_id="29-013", deployment_id="dep-a")
    g.consume_action_token(_looks_right_tok(g, sess.session_id), user_id="1", chat_id="29-013")
    tok = _send_tok(g, sess.session_id)
    sess.deployment_id = "dep-b"
    r = g.consume_action_token(tok, user_id="1", chat_id="29-013")
    assert r["http_status"] == spy["http_status"]
    assert "deployment" in r["message"].lower()
    assert transport.calls == []


def test_act_014_draft_hash_mismatch_409() -> None:
    spy = _spy("act-reject-409")
    g, transport = _guard_recording()
    sess = g.get_or_create_session(user_id="1", chat_id="29-014")
    g.consume_action_token(_looks_right_tok(g, sess.session_id), user_id="1", chat_id="29-014")
    tok = _send_tok(g, sess.session_id, draft_hash="a" * 64)
    sess.draft_hash = "b" * 64
    r = g.consume_action_token(tok, user_id="1", chat_id="29-014")
    assert r["http_status"] == spy["http_status"]
    assert "draft" in r["message"].lower()
    assert transport.calls == []


def test_act_015_frozen_missing_409_no_gateway() -> None:
    spy = _spy("act-reject-409")
    g, transport = _guard_recording()
    sess = g.get_or_create_session(user_id="1", chat_id="29-015")
    g.consume_action_token(_looks_right_tok(g, sess.session_id), user_id="1", chat_id="29-015")
    tok = _send_tok(g, sess.session_id)
    sess.frozen_tool_intent = None
    r = g.consume_action_token(tok, user_id="1", chat_id="29-015")
    assert r["http_status"] == spy["http_status"]
    assert "frozen" in r["message"].lower()
    assert transport.calls == []


def test_act_016_illegal_fsm_409() -> None:
    spy = _spy("act-reject-409")
    g, transport = _guard_recording()
    sess = g.get_or_create_session(user_id="1", chat_id="29-016")
    tok = _looks_right_tok(g, sess.session_id)
    rec = g.tokens.lookup(tok)
    # Align expected_state with a session state where CONFIRM_INTERPRETATION is illegal.
    sess.state = SessionState.INTERVIEWING
    rec.expected_state = SessionState.INTERVIEWING.value
    r = g.consume_action_token(tok, user_id="1", chat_id="29-016")
    assert r["http_status"] == spy["http_status"]
    assert "transition" in r["message"].lower() or r["code"] == spy["error_code"]
    assert transport.calls == []


def test_act_017_hash_only_persist_no_raw() -> None:
    spy = _spy("act-hash-only-persist")
    store = ActionTokenStore()
    raw, rec = store.issue(
        action=TokenActionKind.CONFIRM_INTERPRETATION,
        session_id="s-act-017",
        user_id="1",
        chat_id="29-017",
        deployment_id="local",
        revision=1,
        expected_state="awaiting_interpretation_confirm",
    )
    assert spy["raw_stored"] is False
    assert spy["forbid_substrings_in_store_keys"] is True
    keys = list(store._by_hash.keys())  # type: ignore[attr-defined]
    assert raw not in keys
    assert all(raw not in str(k) for k in keys)
    assert hash_token(raw) in store._by_hash  # type: ignore[attr-defined]
    snap = store.bind_snapshot(raw)
    assert snap["raw_stored"] is False
    assert "raw" not in snap
    assert snap["token_hash"] == rec.token_hash
    # Optional log/forbid bag — snapshot-like persist must never carry raw.
    log_bag = [json.dumps(snap, sort_keys=True)]
    assert all(raw not in line for line in log_bag)
    for _ in range(10):
        assert len(mint_opaque_token().encode("utf-8")) <= spy["mint_max_utf8_bytes"]


class _FakePgConn:
    """Minimal conn for PostgresActionTokenStore.issue/peek without live PG."""

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


def test_act_017_pg_store_hash_only_no_raw_in_insert() -> None:
    """G-01: PostgresActionTokenStore persists hash only (fake conn seam)."""
    spy = _spy("act-hash-only-persist")
    fake = _FakePgConn()
    store = PostgresActionTokenStore(
        "postgresql://fake/aibridge_test",
        conn=fake,
    )
    raw, rec = store.issue(
        action=TokenActionKind.CONFIRM_INTERPRETATION,
        session_id="s-act-017-pg",
        user_id="1",
        chat_id="29-017-pg",
        deployment_id="local",
        revision=1,
        expected_state="awaiting_interpretation_confirm",
    )
    assert spy["raw_stored"] is False
    assert spy["forbid_substrings_in_store_keys"] is True
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


def test_act_001_fixture_expect_ssot_after_mint_replace() -> None:
    """G-02: channel fixture expect is SSOT after PLACEHOLDER mint-replace."""
    env = load_fixture("channel", "act-looks-right")
    expect = env["payload"]["expect"]
    body = dict(env["payload"]["body"])
    assert body["action_token"] == "PLACEHOLDER_TOKEN"
    g, transport = _guard_recording()
    uid, cid = body["principal"]["user_id"], body["principal"]["chat_id"]
    sess = g.get_or_create_session(user_id=uid, chat_id=cid)
    body["action_token"] = _looks_right_tok(g, sess.session_id)
    r = g.consume_action_token(body["action_token"], user_id=uid, chat_id=cid)
    assert r["http_status"] == expect["http_status"]
    assert r["state"] == expect["state"]
    assert r["gateway_invocations"] == expect["gateway_call_count"]
    assert transport.calls == []


def test_act_005_fixture_expect_ssot_random_token() -> None:
    """G-02: ACT-005 envelope body+expect drive unit reject path."""
    env = load_fixture("channel", "act-random-token")
    expect = env["payload"]["expect"]
    body = dict(env["payload"]["body"])
    g, transport = _guard_recording()
    r = g.consume_action_token(
        body["action_token"],
        user_id=body["principal"]["user_id"],
        chat_id=body["principal"]["chat_id"],
    )
    assert r["http_status"] == expect["http_status"]
    assert r["code"] == expect["error_code"]
    assert transport.calls == []


def test_act_018_mint_tokens_le_64_bytes() -> None:
    spy = _spy("act-hash-only-persist")
    for _ in range(20):
        assert 1 <= len(mint_opaque_token().encode("utf-8")) <= spy["mint_max_utf8_bytes"]
    # façade 422 envelope present (HTTP covered in integration)
    env = load_fixture("channel", "act-token-len-65")
    assert env["payload"]["expect"]["http_status"] == 422
    assert len(env["payload"]["body"]["action_token"].encode("utf-8")) == 65
