"""STORY-AIBRIDGE-36 — N8N-WF-001 pin pointer honesty (no invent export / no live TG).

Claims from fixture-index pin pointer + Layer E adapter-contract labeling.
Out-of-CI smoke remains optional (default_ci=false).
P6 audit: ops TRACEABILITY sync · guide Layer E · fixture-index stories_covered 35–36.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from fixture_loader import FIXTURES_ROOT, load_fixture

BRIDGE_ROOT = Path(__file__).resolve().parent.parent
PKG_PIN = (
    BRIDGE_ROOT
    / "docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/fixtures/meta/n8n-wf-001-pin-pointer.json"
)
PKG_TRACE = (
    BRIDGE_ROOT
    / "docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/TRACEABILITY-MATRIX.md"
)
OPS_TRACE = BRIDGE_ROOT / "docs/qa/inbound-outbound/TRACEABILITY-MATRIX.md"
GUIDE = (
    BRIDGE_ROOT
    / "docs/tasks/qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md"
)
PKG_INDEX = (
    BRIDGE_ROOT
    / "docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/fixtures/fixture-index.json"
)
EXPORT_REL = "docs/ops/n8n-channel-workflow/exports/aibridge-telegram-channel-v1.json"
STORY_35 = "STORY-AIBRIDGE-35-qa-gates-layers-dod"
STORY_36 = "STORY-AIBRIDGE-36-qa-n8n-workflow-contract-honesty"


def _n8n_wf_001_coverage(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("| N8N-WF-001 |"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            return cells[-1] if cells else ""
    raise AssertionError("N8N-WF-001 row missing")


def test_n8n_wf_001_pin_pointer_promoted_hash_eq() -> None:
    assert PKG_PIN.is_file(), "package pin pointer missing"
    promoted = FIXTURES_ROOT / "meta" / "n8n-wf-001-pin-pointer.json"
    assert promoted.is_file(), "tests/fixtures/meta/n8n-wf-001-pin-pointer.json missing"
    assert hashlib.sha256(PKG_PIN.read_bytes()).hexdigest() == hashlib.sha256(
        promoted.read_bytes()
    ).hexdigest()


def test_n8n_wf_001_pin_deferred_or_sha_bound() -> None:
    """Honest coverage: deferred without inventing export, or sha256 when file present."""
    env = load_fixture("meta", "n8n-wf-001-pin-pointer")
    assert env["schema_version"] == "1.0"
    assert env["fixture_id"] == "meta.n8n-wf-001-pin-pointer"
    assert "N8N-WF-001" in env["matrix_ids"]
    payload = env["payload"]
    assert payload.get("layer_e_label") == "adapter-contract"
    assert payload.get("default_ci") is False
    export_path = BRIDGE_ROOT / EXPORT_REL
    if payload.get("status") == "deferred":
        assert payload.get("defer_reason"), "deferred requires reason"
        assert payload.get("sha256") is None
        assert not export_path.is_file(), "export present but pointer still deferred"
    else:
        assert payload.get("sha256"), "pinned status requires sha256"
        assert export_path.is_file(), "sha256 set but export missing"
        digest = hashlib.sha256(export_path.read_bytes()).hexdigest()
        assert digest == payload["sha256"]


def test_layer_e_adapter_contract_suite_exists() -> None:
    """Layer E default CI is adapter-contract suite — not workflow JSON execution."""
    suite = BRIDGE_ROOT / "tests/n8n/test_n8n_telegram_mapping.py"
    assert suite.is_file()
    text = suite.read_text(encoding="utf-8")
    assert "no live Telegram" in text
    assert "never call live Bot API" in text
    assert "load_fixture" in text
    assert "ADR-Q5" in text


def test_ops_traceability_n8n_wf_001_matches_package_ssot() -> None:
    """G-02: ops copy Coverage cell for N8N-WF-001 matches package SSOT."""
    assert PKG_TRACE.is_file() and OPS_TRACE.is_file()
    pkg_cov = _n8n_wf_001_coverage(PKG_TRACE.read_text(encoding="utf-8"))
    ops_cov = _n8n_wf_001_coverage(OPS_TRACE.read_text(encoding="utf-8"))
    assert pkg_cov == ops_cov
    assert "deferred" in pkg_cov
    assert "open (Scaffolded)" not in ops_cov


def test_guide_layer_e_adapter_contract_honesty() -> None:
    """G-03: guide Layer E labeled adapter-contract with STORY-36 / N8N-WF-001 pointer."""
    text = GUIDE.read_text(encoding="utf-8")
    assert "### Layer E — n8n adapter-contract tests" in text
    assert "adapter-contract" in text
    assert "not** live n8n workflow e2e" in text
    assert "STORY-AIBRIDGE-36" in text
    assert "N8N-WF-001" in text
    assert "TECH §5.1" in text


def test_fixture_index_stories_covered_includes_35_36() -> None:
    """G-04: envelope story_keys + stats.stories_covered include STORY-35/36; hash_eq."""
    assert PKG_INDEX.is_file()
    promoted = FIXTURES_ROOT / "meta" / "fixture-index.json"
    assert promoted.is_file()
    assert hashlib.sha256(PKG_INDEX.read_bytes()).hexdigest() == hashlib.sha256(
        promoted.read_bytes()
    ).hexdigest()
    env = json.loads(promoted.read_text(encoding="utf-8"))
    assert STORY_35 in env.get("story_keys", [])
    assert STORY_36 in env.get("story_keys", [])
    covered = env["payload"]["stats"]["stories_covered"]
    assert STORY_35 in covered
    assert STORY_36 in covered
    assert env["payload"]["stats"]["fixture_count"] == len(env["payload"]["fixtures"])
    assert env["payload"]["stats"]["synced_at"]
