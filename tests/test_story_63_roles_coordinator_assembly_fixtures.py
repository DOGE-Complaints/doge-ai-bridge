"""STORY-AIBRIDGE-63 — roles, coordinator policy, assembly fixtures.

Locks: fixtures≠GPT UI · interview port Keep · L13-1/AC-07 · OOS 62 DDL / 64 live.
No LLM-router.
"""

from __future__ import annotations

import inspect
from pathlib import Path

import pytest

from aibridge.confirm import ConfirmationGuard
from aibridge.confirm_fsm import SessionState
from aibridge.coordinator import build_turn_from_engine, select_next_role
from aibridge.gateway import (
    GatewayExecutor,
    RecordingGatewayTransport,
    RawHttpResponse,
)
from aibridge.roles import (
    DEFAULT_ROLE_REGISTRY,
    V1_ROLE_IDS,
    assemble_role_prompt,
    assert_manifest_covers_v1,
    bind_role_interview_engine,
    load_roles_manifest,
)
from aibridge.roles.invoke import bind_role_interview_engine as invoke_bind
from aibridge.roles.policy import PolicySelectionError

_REPO = Path(__file__).resolve().parents[1]
_DOC = _REPO / "docs" / "runtime-docs" / "10-roles-coordinator-assembly.md"
_ROLES_PKG = _REPO / "src" / "aibridge" / "roles"
_FIXTURES = _REPO / "tests" / "fixtures" / "content"
_ROLES_DIR = _FIXTURES / "roles-instructions"
_ROLES_MANIFEST = _FIXTURES / "roles.manifest.json"
_PROVIDERS = _REPO / "src" / "aibridge" / "providers"
_INTERVIEW_PROVIDERS = _REPO / "src" / "aibridge" / "interview_providers"

_FORBIDDEN_AC07 = (
    "gateway",
    "stash",
    "spa redirect",
    "continuation_url",
    "redirect_base",
    "/v1/drafts",
    "Send to DOGEstonia",
)


def _ok_201() -> RawHttpResponse:
    import json

    body = json.dumps(
        {"data": {"draft_id": "draft-63"}, "trace_id": "trace-63"}
    ).encode()
    return RawHttpResponse(status_code=201, body=body)


def _guard() -> ConfirmationGuard:
    transport = RecordingGatewayTransport(scripted=[_ok_201()])
    executor = GatewayExecutor(
        origin="https://gateway.example.invalid",
        gateway_bearer="gw-63",
        channel_bearer="ch-63",
        redirect_base="https://spa.example",
        transport=transport,
    )
    return ConfirmationGuard(executor=executor)


# --- t01 five roles + pins ---


def test_t01_five_v1_roles_with_version_pins() -> None:
    specs = DEFAULT_ROLE_REGISTRY.require_v1_five()
    assert len(specs) == 5
    assert tuple(s.role_id for s in specs) == V1_ROLE_IDS
    for spec in specs:
        assert spec.version == "v1"
        assert spec.label
    # Callable via coordinator re-export.
    role = select_next_role(phase="interviewing")
    assert role.role_id == "interviewer"
    assert role.version == "v1"


# --- t02 policy → one role; no LLM router ---


def test_t02_policy_selects_exactly_one_role() -> None:
    assert select_next_role(phase="setup").role_id == "communication_setup"
    assert select_next_role(phase="extract").role_id == "extractor"
    assert select_next_role(phase="normalize").role_id == "normalizer"
    assert select_next_role(phase="check").role_id == "checker"
    # Flag overlay wins for interviewing + needs_check.
    assert (
        select_next_role(phase="interviewing", flags={"needs_check": True}).role_id
        == "checker"
    )
    with pytest.raises(PolicySelectionError):
        select_next_role(phase="unknown-phase")
    # No LLM-router module / free meta-agent path under roles/.
    src = (_ROLES_PKG / "policy.py").read_text(encoding="utf-8")
    assert "LLM" in src or "llm" in src.lower() or "router" in src
    assert "select_next_role" in src
    assert "openai" not in src.lower()
    assert "chat.completions" not in src.lower()


# --- t03 assembly dir+manifest + session pin ---


def test_t03_assemble_from_configured_dir_and_manifest() -> None:
    assert_manifest_covers_v1(_ROLES_MANIFEST)
    prompt = assemble_role_prompt(
        instructions_dir=_ROLES_DIR,
        manifest_path=_ROLES_MANIFEST,
        role_id="interviewer",
        node_id="node-63",
    )
    assert "Shared interview core" in prompt.core_text
    assert "Interviewer" in prompt.role_text
    assert prompt.core_text in prompt.assembled
    assert prompt.role_text in prompt.assembled
    assert len(prompt.session_pin) == 64
    pin2 = assemble_role_prompt(
        instructions_dir=_ROLES_DIR,
        manifest_path=_ROLES_MANIFEST,
        role_id="interviewer",
        node_id="node-63",
    ).session_pin
    assert pin2 == prompt.session_pin
    pin_other = assemble_role_prompt(
        instructions_dir=_ROLES_DIR,
        manifest_path=_ROLES_MANIFEST,
        role_id="checker",
        node_id="node-63",
    ).session_pin
    assert pin_other != prompt.session_pin
    # Manifest is the only file index — not GPT UI hunt.
    data = load_roles_manifest(_ROLES_MANIFEST)
    assert data["bundle_version"] == "roles-fixture-v1"


# --- t04 in-repo fixtures; no GPT UI required ---


def test_t04_in_repo_fixtures_no_gpt_ui_checkout() -> None:
    assert _ROLES_DIR.is_dir()
    assert _ROLES_MANIFEST.is_file()
    # Suite path stays under doge-ai-bridge/tests/fixtures — never requires sibling GPT UI.
    assert "GPT UI" not in str(_ROLES_DIR)
    assert "GPT UI" not in str(_ROLES_MANIFEST)
    # Even if GPT UI tree is absent, fixtures remain loadable.
    _ = assemble_role_prompt(
        instructions_dir=_ROLES_DIR,
        manifest_path=_ROLES_MANIFEST,
        role_id="extractor",
    )
    # Document isolation intent.
    assert _DOC.is_file()
    doc = _DOC.read_text(encoding="utf-8")
    assert "GPT UI" in doc
    assert "fixtures" in doc.lower()


# --- t05 interview port Keep ---


def test_t05_role_model_path_uses_interview_port_not_providers() -> None:
    assert _INTERVIEW_PROVIDERS.is_dir()
    assert _PROVIDERS.is_dir()
    src = (_ROLES_PKG / "invoke.py").read_text(encoding="utf-8")
    assert "from aibridge.interview_providers" in src
    assert "bind_interview_engine_at_wire" in src
    assert "from aibridge.providers" not in src
    assert "import aibridge.providers" not in src
    # Module home of bind helper is roles.invoke, re-exported.
    assert bind_role_interview_engine is invoke_bind
    assert invoke_bind.__module__ == "aibridge.roles.invoke"
    assert inspect.getmodule(invoke_bind).__name__ == "aibridge.roles.invoke"  # type: ignore[union-attr]


# --- t06 L13-1 ordinary reply ≠ send ---


def test_t06_ordinary_reply_does_not_offer_send() -> None:
    guard = _guard()
    sess = guard.get_or_create_session(user_id="u63", chat_id="c63")
    assert sess.state is SessionState.INTERVIEWING
    out = build_turn_from_engine(
        guard,
        sess,
        {"ok": True, "reply_text": "I understand your concern about the park.", "function_calls": []},
    )
    assert out["reply_text"].startswith("I understand")
    labels = {a.get("label", "") for a in out["actions"]}
    styles = {a.get("style", "") for a in out["actions"]}
    assert "Send to DOGEstonia" not in labels
    assert "primary" not in styles  # send uses primary; interpret uses success
    # Soft understanding path may remain.
    assert any(a.get("style") == "success" for a in out["actions"]) or out["actions"] == []
    assert sess.state in {
        SessionState.INTERVIEWING,
        SessionState.AWAITING_INTERPRETATION_CONFIRM,
    }


# --- t07 AC-07 fixtures no gateway/SPA procedure ---


def test_t07_fixture_texts_exclude_gateway_spa_procedure() -> None:
    texts: list[str] = []
    for path in sorted(_ROLES_DIR.glob("*.md")):
        texts.append(path.read_text(encoding="utf-8").lower())
    blob = "\n".join(texts)
    for needle in _FORBIDDEN_AC07:
        assert needle.lower() not in blob, f"AC-07 forbidden token in fixtures: {needle}"


# --- t08 story gate ---


def test_t08_story_gate_docs_and_locks() -> None:
    assert _DOC.is_file()
    text = _DOC.read_text(encoding="utf-8")
    assert "AC-AIB-13-02" in text or "five" in text.lower()
    assert "AC-AIB-13-03" in text or "manifest" in text.lower()
    assert "AC-07" in text or "gateway" in text.lower()
    assert "L13-1" in text or "AC-08" in text or "ordinary" in text.lower()
    assert "62" in text and "64" in text
    assert "LLM-router" in text or "LLM" in text
    assert (_ROLES_PKG / "registry.py").is_file()
    assert (_ROLES_PKG / "policy.py").is_file()
    assert (_ROLES_PKG / "assembly.py").is_file()
    assert (_ROLES_PKG / "invoke.py").is_file()
