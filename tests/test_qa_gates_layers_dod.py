"""STORY-AIBRIDGE-35 — Gate-1…5 + CHAR-001…008 + layers A–F checklist (program DoD).

Claims are from existing suite paths / fixture-index / acceptance PASS artifacts —
no live Telegram / Railway invent. Gate-5 / Layer F: deferred_live. Layer D: deferred+bound.
CHAR-*: characterization capture-first with refs or defer_reason.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from fixture_loader import FIXTURES_ROOT, load_fixture

ROOT = Path(__file__).resolve().parent
BRIDGE_ROOT = ROOT.parent
REPO_ROOT = BRIDGE_ROOT.parent
PKG_INDEX = (
    BRIDGE_ROOT
    / "docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/fixtures/fixture-index.json"
)

# Gate → existing automated suite evidence (paths verified on disk; no product invent here).
GATE_MUST_EVIDENCE: dict[str, tuple[str, ...]] = {
    "Gate-1": (
        "tests/contract/test_auth_ops_boundaries.py",
        "tests/contract/test_json_schema_boundary.py",
        "tests/n8n/test_n8n_telegram_mapping.py",
        "tests/test_contract_oas.py",
    ),
    "Gate-2": (
        "tests/test_responses_store_false.py",
        "tests/integration/test_idempotency_concurrency.py",
        "tests/unit/test_tool_call_validation.py",
        "tests/integration/test_openai_prompt_behavior.py",
    ),
    "Gate-3": (
        "tests/unit/test_action_token_fsm.py",
        "tests/integration/test_action_token_fsm_http.py",
        "tests/integration/test_gateway_continuation.py",
        "tests/test_gateway_outcomes.py",
    ),
    "Gate-4": (
        "tests/integration/test_lifecycle_retention.py",
        "tests/contract/test_readyz_configuration.py",
        "tests/integration/test_privacy_observability.py",
        "tests/test_story_09_postgres_ssot.py",
    ),
}

CHAR_IDS = tuple(f"CHAR-{i:03d}" for i in range(1, 9))

# Layer A–E dirs required in default CI; D deferred+bound; F deferred.
LAYER_DIRS: dict[str, Path | None] = {
    "A_unit": ROOT / "unit",
    "B_contract": ROOT / "contract",
    "C_integration": ROOT / "integration",
    "E_n8n": ROOT / "n8n",
    "F_live": None,  # deferred — out of default CI
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _repo_path(rel: str) -> Path:
    """Resolve path relative to doge-ai-bridge/ or repo root."""
    cand = BRIDGE_ROOT / rel
    if cand.is_file() or cand.is_dir():
        return cand
    cand2 = REPO_ROOT / rel
    if cand2.is_file() or cand2.is_dir():
        return cand2
    return Path(rel)


def test_fixture_index_promoted_hash_eq_package() -> None:
    """ADR-Q1 promote=copy: package original intact and hash_eq vs tests/fixtures/meta/."""
    assert PKG_INDEX.is_file(), "package fixtures/fixture-index.json missing"
    promoted = FIXTURES_ROOT / "meta" / "fixture-index.json"
    assert promoted.is_file(), "tests/fixtures/meta/fixture-index.json missing"
    assert _sha256(PKG_INDEX) == _sha256(promoted)


def test_fixture_index_envelope_and_stories_23_34() -> None:
    env = load_fixture("meta", "fixture-index")
    assert env["schema_version"] == "1.0"
    assert env["fixture_id"] == "meta.fixture-index"
    assert env["cluster"] == "meta"
    rows = env["payload"]["fixtures"]
    assert len(rows) >= 200, f"expected synced promoted fixtures, got {len(rows)}"
    stories = {sk for r in rows for sk in r.get("story_keys", [])}
    for n in range(23, 35):
        assert any(f"STORY-AIBRIDGE-{n}-" in s for s in stories), f"story {n} missing from index"
    for path_rel in (r["path"] for r in rows):
        assert (FIXTURES_ROOT / path_rel).is_file(), f"indexed path missing: {path_rel}"


@pytest.mark.parametrize("gate_id", sorted(GATE_MUST_EVIDENCE))
def test_gate_must_evidence_modules_exist(gate_id: str) -> None:
    """Gate-1…4 must-rows: bound suite modules present on disk (claims from code tree)."""
    for rel in GATE_MUST_EVIDENCE[gate_id]:
        assert (BRIDGE_ROOT / rel).is_file(), f"{gate_id}: missing evidence {rel}"


@pytest.mark.parametrize("gate_id", sorted(GATE_MUST_EVIDENCE))
def test_gate_program_evidence_bound_to_suites_and_acceptance(gate_id: str) -> None:
    """G-01: program.gates mirrors suite modules + acceptance PASS artifacts (not is_file-only)."""
    env = load_fixture("meta", "fixture-index")
    gate = next(g for g in env["payload"]["program"]["gates"] if g["id"] == gate_id)
    assert gate["status"] == "must"
    assert gate["evidence_mode"] == "suite_modules_plus_acceptance"
    assert tuple(gate["evidence_paths"]) == GATE_MUST_EVIDENCE[gate_id]
    for rel in gate["evidence_paths"]:
        assert (BRIDGE_ROOT / rel).is_file(), f"{gate_id}: evidence missing {rel}"
    assert gate.get("acceptance_paths"), f"{gate_id}: acceptance_paths required"
    for rel in gate["acceptance_paths"]:
        path = _repo_path(rel)
        assert path.is_file(), f"{gate_id}: acceptance missing {rel}"
        text = path.read_text(encoding="utf-8")
        assert "**PASS**" in text or "| **PASS** |" in text or "PASS" in text, (
            f"{gate_id}: acceptance not PASS: {rel}"
        )


def test_gate5_live_deferred_out_of_default_ci() -> None:
    """Gate-5 / Layer F — explicit defer; no live TG / Railway SUCCESS invent in default CI."""
    env = load_fixture("meta", "fixture-index")
    program = env["payload"]["program"]
    gate5 = next(g for g in program["gates"] if g["id"] == "Gate-5")
    assert gate5["status"] == "deferred_live"
    assert "live" in gate5["reason"].lower()
    assert LAYER_DIRS["F_live"] is None
    assert program["layers"]["F_live"]["status"] == "deferred_live"


@pytest.mark.parametrize("char_id", CHAR_IDS)
def test_char_capture_first_bound_refs_or_defer(char_id: str) -> None:
    """G-03: CHAR-001…008 have refs/bound_tests or defer_reason — capture-first, no product invent."""
    env = load_fixture("meta", "fixture-index")
    assert char_id in env["matrix_ids"]
    chars = {c["id"]: c for c in env["payload"]["program"]["characterization"]}
    row = chars[char_id]
    assert row["status"] in (
        "characterization",
        "decision_recorded",
    ), f"{char_id}: unexpected status {row['status']!r}"
    assert "capture-first" in row["policy"] or "Option A" in row.get("policy", "")
    refs = row.get("refs") or []
    bound = row.get("bound_tests") or []
    defer = row.get("defer_reason")
    assert refs or defer, f"{char_id}: need refs or defer_reason"
    assert bound, f"{char_id}: bound_tests required"
    for rel in refs:
        assert (FIXTURES_ROOT / rel).is_file(), f"{char_id}: missing fixture ref {rel}"
    for rel in bound:
        assert (BRIDGE_ROOT / rel).is_file(), f"{char_id}: missing bound_test {rel}"
    if char_id == "CHAR-008":
        assert defer, "CHAR-008 must document defer_reason while export/capture incomplete"
        # Behavioral path: capture envelope exists and is honest (deferred XOR filled).
        cap = load_fixture("n8n", "char-008-send-edit-capture")
        assert cap["payload"]["status"] in ("deferred", "captured")
        if cap["payload"]["status"] == "deferred":
            assert (cap["payload"].get("defer_reason") or "").strip()
            assert cap["payload"].get("response_states") == []
        else:
            assert cap["payload"].get("response_states")
            assert (cap["payload"].get("retry_dedupe_policy") or "").strip()


@pytest.mark.parametrize("layer_key", ["A_unit", "B_contract", "C_integration", "E_n8n"])
def test_layer_directories_present(layer_key: str) -> None:
    """TECH §5.1 — required layer dirs present for default CI scope."""
    path = LAYER_DIRS[layer_key]
    assert path is not None and path.is_dir(), f"missing layer dir for {layer_key}"
    assert any(path.glob("test_*.py")), f"no test_*.py under {path}"


def test_layer_d_deferred_with_bound_evidence() -> None:
    """G-02: Layer D explicit deferred + bound Dockerfile/STORY-21/22 proofs (assert-only)."""
    env = load_fixture("meta", "fixture-index")
    layer_d = env["payload"]["program"]["layers"]["D_container"]
    assert layer_d["status"] == "deferred"
    assert "container" in layer_d["reason"].lower() or "image" in layer_d["reason"].lower()
    assert layer_d.get("evidence_paths"), "Layer D evidence_paths required"
    for rel in layer_d["evidence_paths"]:
        path = _repo_path(rel)
        assert path.is_file(), f"Layer D evidence missing: {rel}"


def test_program_gates_checklist_complete() -> None:
    env = load_fixture("meta", "fixture-index")
    ids = {g["id"] for g in env["payload"]["program"]["gates"]}
    assert ids == {"Gate-1", "Gate-2", "Gate-3", "Gate-4", "Gate-5"}
    char_ids = {c["id"] for c in env["payload"]["program"]["characterization"]}
    assert char_ids == set(CHAR_IDS)
    layers = env["payload"]["program"]["layers"]
    assert set(layers) >= {"A_unit", "B_contract", "C_integration", "D_container", "E_n8n", "F_live"}
