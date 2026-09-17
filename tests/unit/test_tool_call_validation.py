"""STORY-AIBRIDGE-28 — TOOL-001…014 tool-call validation (unit; no live Telegram).

Fixture-driven validate_function_calls / build_turn_from_engine / register_session_call.
TOOL-014: register_session_call duplicate is must; coordinator→session_call wiring
capture-first (characterization) — no silent product invent.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import pytest

from aibridge.confirm import ConfirmationGuard
from aibridge.confirm_fsm import SessionState
from aibridge.coordinator import (
    ToolValidationError,
    ValidationContext,
    build_turn_from_engine,
    persist_pending_tool,
    validate_function_calls,
)
from aibridge.gateway import GatewayExecutor, RecordingGatewayTransport, RawHttpResponse
from aibridge.pg_runtime import register_session_call
from aibridge.request_assembly import ServerConstants
from aibridge.tool_gen import CANONICAL_OPERATION_ID
_TESTS_ROOT = Path(__file__).resolve().parents[1]
if str(_TESTS_ROOT) not in sys.path:
    sys.path.insert(0, str(_TESTS_ROOT))
from fixture_loader import load_fixture  # noqa: E402

STORY = "STORY-AIBRIDGE-28-qa-tool-call-validation"
TOOL_IDS = {f"TOOL-{i:03d}" for i in range(1, 15)}
PKG_FIXTURES = (
    _TESTS_ROOT.parents[0]
    / "docs"
    / "tasks"
    / "backlog-stories"
    / "qa-inbound-outbound-data-flow"
    / "fixtures"
)


def _hash(path: Path) -> bytes:
    return hashlib.sha256(path.read_bytes()).digest()


def _ctx(*, strict_wire: bool = False) -> ValidationContext:
    env = load_fixture("gateway", "tool-validation-context")
    p = env["payload"]
    wire = p["wire_schema_strict_for_tool011"] if strict_wire else p["wire_schema"]
    c = p["constants"]
    return ValidationContext(
        tool_parameters=p["tool_parameters"],
        pack_schema=p["pack_schema"],
        wire_schema=wire,
        constants=ServerConstants(
            schema_version=c["schema_version"],
            schema_id=c["schema_id"],
            schema_version_pack=c["schema_version_pack"],
            origin_source=c["origin_source"],
        ),
    )


def _fcs_from_openai(name: str) -> list[dict[str, Any]]:
    env = load_fixture("openai", name)
    body = env["payload"]["body"]
    out: list[dict[str, Any]] = []
    for item in body.get("output") or []:
        if item.get("type") == "function_call":
            out.append(
                {
                    "call_id": item.get("call_id") or "",
                    "name": item.get("name") or "",
                    "arguments": item.get("arguments"),
                }
            )
    return out


def _engine_result_from_openai(name: str) -> dict[str, Any]:
    env = load_fixture("openai", name)
    body = env["payload"]["body"]
    fcs = _fcs_from_openai(name)
    reply = "Acknowledged."
    for item in body.get("output") or []:
        if item.get("type") == "message":
            for c in item.get("content") or []:
                if c.get("type") == "output_text":
                    reply = str(c.get("text") or reply)
    return {
        "ok": True,
        "reply_text": reply,
        "function_calls": fcs,
        "replay_items": list(body.get("output") or []),
    }


def _stash_raw() -> RawHttpResponse:
    env = load_fixture("gateway", "tool-stash-201")
    p = env["payload"]
    return RawHttpResponse(
        status_code=int(p["status_code"]),
        body=json.dumps(p["body"]).encode(),
    )


def _guard_with_validation() -> ConfirmationGuard:
    transport = RecordingGatewayTransport(scripted=[_stash_raw()])
    executor = GatewayExecutor(
        origin="https://gateway.example.invalid",
        gateway_bearer="gw",
        channel_bearer="ch",
        transport=transport,
        redirect_base="https://spa.example",
    )
    return ConfirmationGuard(
        executor=executor,
        validation_context=_ctx(),
    )

def test_fixtures_promoted_hash_eq_and_matrix_coverage() -> None:
    names_openai = [
        "tool-fc-valid",
        "tool-fc-before-confirm",
        "tool-fc-two-calls",
        "tool-fc-unknown-name",
        "tool-fc-missing-call-id",
        "tool-fc-malformed-args",
        "tool-fc-args-array",
        "tool-fc-args-scalar",
        "tool-fc-gate1-fail",
        "tool-fc-missing-payload",
        "tool-fc-pack-violate",
        "tool-fc-wire-violate",
        "tool-fc-server-override",
    ]
    names_gateway = ["tool-validation-context", "tool-stash-201"]
    seen: set[str] = set()
    for cluster, names in (("openai", names_openai), ("gateway", names_gateway)):
        for name in names:
            env = load_fixture(cluster, name)
            assert env["schema_version"] == "1.0"
            assert STORY in env["story_keys"]
            seen.update(env["matrix_ids"])
            pkg = PKG_FIXTURES / f"{name}.json"
            copy = _TESTS_ROOT / "fixtures" / cluster / f"{name}.json"
            assert pkg.is_file() and copy.is_file()
            assert _hash(pkg) == _hash(copy)
    assert TOOL_IDS.issubset(seen)


def test_tool_001_fc_before_looks_right_blocked_no_send() -> None:
    guard = _guard_with_validation()
    sess = guard.get_or_create_session(user_id="1", chat_id="28-001")
    assert sess.state is SessionState.INTERVIEWING
    out = build_turn_from_engine(guard, sess, _engine_result_from_openai("tool-fc-before-confirm"))
    assert out["actions"] == []
    assert "blocked until interpretation" in out["reply_text"]
    assert sess.frozen_tool_intent is None
    assert sess.pending_call_id is None
    assert guard.executor.transport.calls == []  # type: ignore[union-attr]


def test_tool_002_single_allowed_call_gates_freeze_send() -> None:
    guard = _guard_with_validation()
    sess = guard.get_or_create_session(user_id="1", chat_id="28-002")
    acts = guard.offer_interpretation_confirm(sess.session_id)
    tok = next(a["token"] for a in acts if a["style"] == "success")
    guard.consume_action_token(tok, user_id="1", chat_id="28-002")
    assert sess.state is SessionState.INTERPRETATION_CONFIRMED

    frozen = validate_function_calls(
        _fcs_from_openai("tool-fc-valid"),
        session_state=sess.state,
        validation=_ctx(),
    )
    assert frozen["name"] == CANONICAL_OPERATION_ID
    assert frozen["arguments"]["schema_binding"]["schema_id"] == "uus_veerenni_civic"
    assert frozen["arguments"]["schema_binding"]["schema_version"] == "v3"
    assert frozen["arguments"]["origin"]["source"] == "openai_responses_telegram"

    out = build_turn_from_engine(guard, sess, _engine_result_from_openai("tool-fc-valid"))
    assert len(out["actions"]) == 3
    labels = {a["label"] for a in out["actions"]}
    assert "Send to DOGEstonia" in labels
    assert sess.frozen_tool_intent is not None
    assert sess.pending_call_id == "call_tool_valid"
    assert sess.state is SessionState.AWAITING_SEND_CONFIRM
    assert guard.executor.transport.calls == []  # type: ignore[union-attr]


@pytest.mark.parametrize(
    ("fixture", "match"),
    [
        ("tool-fc-two-calls", "Exactly one"),
        ("tool-fc-unknown-name", "not allowlisted"),
        ("tool-fc-missing-call-id", "missing call_id"),
        ("tool-fc-malformed-args", "Malformed"),
        ("tool-fc-args-array", "JSON object"),
        ("tool-fc-args-scalar", "JSON object"),
    ],
)
def test_tool_003_007_reject_shapes(fixture: str, match: str) -> None:
    with pytest.raises(ToolValidationError, match=match):
        validate_function_calls(
            _fcs_from_openai(fixture),
            session_state=SessionState.INTERPRETATION_CONFIRMED,
            validation=_ctx(),
        )


def test_tool_008_gate1_fail_before_freeze() -> None:
    with pytest.raises(ToolValidationError, match="gate1"):
        validate_function_calls(
            _fcs_from_openai("tool-fc-gate1-fail"),
            session_state=SessionState.INTERPRETATION_CONFIRMED,
            validation=_ctx(),
        )


def test_tool_009_missing_structured_payload_gate2() -> None:
    with pytest.raises(ToolValidationError, match="gate2"):
        validate_function_calls(
            _fcs_from_openai("tool-fc-missing-payload"),
            session_state=SessionState.INTERPRETATION_CONFIRMED,
            validation=_ctx(),
        )


def test_tool_010_pack_schema_violate_gate2() -> None:
    with pytest.raises(ToolValidationError, match="gate2"):
        validate_function_calls(
            _fcs_from_openai("tool-fc-pack-violate"),
            session_state=SessionState.INTERPRETATION_CONFIRMED,
            validation=_ctx(),
        )


def test_tool_011_wire_schema_violate_gate3() -> None:
    with pytest.raises(ToolValidationError, match="gate3"):
        validate_function_calls(
            _fcs_from_openai("tool-fc-wire-violate"),
            session_state=SessionState.INTERPRETATION_CONFIRMED,
            validation=_ctx(strict_wire=True),
        )


def test_tool_012_server_owned_fields_stripped_replaced() -> None:
    frozen = validate_function_calls(
        _fcs_from_openai("tool-fc-server-override"),
        session_state=SessionState.INTERPRETATION_CONFIRMED,
        validation=_ctx(),
    )
    args = frozen["arguments"]
    assert args["schema_version"] == "m2.story_intake_envelope.v2"
    assert args["schema_binding"]["schema_id"] == "uus_veerenni_civic"
    assert args["schema_binding"]["schema_version"] == "v3"
    assert args["origin"]["source"] == "openai_responses_telegram"
    assert "gateway_url" not in args


def test_tool_013_persist_failure_no_send_actions() -> None:
    guard = _guard_with_validation()
    sess = guard.get_or_create_session(user_id="1", chat_id="28-013")
    sess.state = SessionState.INTERPRETATION_CONFIRMED

    def _boom(self: ConfirmationGuard, s: Any) -> None:  # noqa: ANN401
        raise RuntimeError("persist boom")

    guard._persist_session = _boom.__get__(guard, ConfirmationGuard)  # type: ignore[method-assign]

    with pytest.raises(RuntimeError, match="persist boom"):
        build_turn_from_engine(guard, sess, _engine_result_from_openai("tool-fc-valid"))
    # Fail closed: no Send / gateway; no in-memory freeze leak (TOOL-013).
    assert guard.executor.transport.calls == []  # type: ignore[union-attr]
    assert sess.state is not SessionState.AWAITING_SEND_CONFIRM
    assert sess.frozen_tool_intent is None
    assert sess.pending_call_id is None
    assert sess.pending_replay_items == []


def test_tool_014_call_id_replay_no_duplicate_consequential() -> None:
    """Must: no gateway on call_id replay without Send.

    Characterization (capture-first): second same call_id while already
    awaiting_send_confirm raises IllegalTransitionError (no remint / no gateway).
    register_session_call is PG store API — not yet wired into coordinator.
    """
    from aibridge.confirm_fsm import IllegalTransitionError

    guard = _guard_with_validation()
    sess = guard.get_or_create_session(user_id="1", chat_id="28-014")
    sess.state = SessionState.INTERPRETATION_CONFIRMED
    out1 = build_turn_from_engine(guard, sess, _engine_result_from_openai("tool-fc-valid"))
    assert any(a.get("label") == "Send to DOGEstonia" for a in out1["actions"])
    assert sess.pending_call_id == "call_tool_valid"

    # Same call_id replay — capture-first current FSM behavior.
    with pytest.raises(IllegalTransitionError):
        build_turn_from_engine(guard, sess, _engine_result_from_openai("tool-fc-valid"))
    # No consequential gateway execution without Send consume.
    assert guard.executor.transport.calls == []  # type: ignore[union-attr]
    assert register_session_call.__name__ == "register_session_call"


def test_reject_paths_expose_no_send_via_build_turn() -> None:
    guard = _guard_with_validation()
    sess = guard.get_or_create_session(user_id="1", chat_id="28-rej")
    sess.state = SessionState.INTERPRETATION_CONFIRMED
    for name in (
        "tool-fc-two-calls",
        "tool-fc-unknown-name",
        "tool-fc-malformed-args",
        "tool-fc-pack-violate",
    ):
        out = build_turn_from_engine(guard, sess, _engine_result_from_openai(name))
        assert out["actions"] == [], name
        assert not any(
            "Send" in str(a.get("label") or "") for a in (out.get("actions") or [])
        )
    assert guard.executor.transport.calls == []  # type: ignore[union-attr]


def test_gateway_oas_pin_present() -> None:
    env = load_fixture("gateway", "tool-validation-context")
    pin = env["payload"]["oas_pin"]
    oas = _TESTS_ROOT.parents[0] / pin["path"]
    assert oas.is_file()
    text = oas.read_text(encoding="utf-8")
    assert pin["operation_id"] in text
    assert pin["schema"] in text
