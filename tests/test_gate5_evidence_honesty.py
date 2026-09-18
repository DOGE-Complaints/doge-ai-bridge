"""STORY-AIBRIDGE-37 — Gate-5 evidence honesty (no invent live TG / Railway SUCCESS).

Default CI keeps deferred_live; evidence index may be deferred capture-first.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

from fixture_loader import FIXTURES_ROOT, load_fixture

BRIDGE_ROOT = Path(__file__).resolve().parent.parent
PKG_EV = (
    BRIDGE_ROOT
    / "docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/fixtures/meta/gate5-evidence-index.json"
)
CHECKLIST = BRIDGE_ROOT / "docs/ops/n8n-channel-workflow/r3-p1-09-live-gate-checklist.md"
STORY_34 = (
    BRIDGE_ROOT
    / "docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-34-qa-product-journey-scenarios.md"
)
OPS_README = BRIDGE_ROOT / "docs/ops/n8n-channel-workflow/README.md"


def test_gate5_evidence_index_promoted_hash_eq() -> None:
    assert PKG_EV.is_file()
    promoted = FIXTURES_ROOT / "meta" / "gate5-evidence-index.json"
    assert promoted.is_file()
    assert hashlib.sha256(PKG_EV.read_bytes()).hexdigest() == hashlib.sha256(
        promoted.read_bytes()
    ).hexdigest()


def test_gate5_evidence_deferred_or_accepted() -> None:
    env = load_fixture("meta", "gate5-evidence-index")
    assert env["schema_version"] == "1.0"
    assert env["fixture_id"] == "meta.gate5-evidence-index"
    assert "Gate-5" in env["matrix_ids"]
    payload = env["payload"]
    assert payload.get("default_ci") is False
    assert payload.get("layer_f_status") == "deferred_live"
    if payload.get("status") == "deferred":
        assert payload.get("defer_reason")
        assert payload.get("accepted_pack") is False
        assert payload.get("evidence_paths") == []
    else:
        assert payload.get("accepted_pack") is True
        assert payload.get("evidence_paths"), "accepted pack requires evidence_paths"


def test_gate5_program_still_deferred_live_in_default_ci() -> None:
    env = load_fixture("meta", "fixture-index")
    gate5 = next(g for g in env["payload"]["program"]["gates"] if g["id"] == "Gate-5")
    assert gate5["status"] == "deferred_live"
    assert env["payload"]["program"]["layers"]["F_live"]["status"] == "deferred_live"


def test_gate5_checklist_and_uc_crosslinks() -> None:
    text = CHECKLIST.read_text(encoding="utf-8")
    assert "Gate-5 — live channel pilot (out of CI)" in text
    assert "gate-5-live-channel-pilot-out-of-ci" in text
    assert "Real Telegram → n8n → private aibridge" in text
    assert "answerCallbackQuery" in text or "Callback acknowledged" in text
    # G3 — staging stash → SPA continuation (guide §15 / checklist)
    assert "SPA continuation URL" in text
    assert "staging" in text.lower()
    assert "stash" in text.lower()
    assert "never claims the draft is published" in text
    assert "Default CI / pytest:** **NO**" in text or "out-of-CI only" in text
    s34 = STORY_34.read_text(encoding="utf-8")
    assert "STORY-AIBRIDGE-37" in s34
    assert "not Gate-5" in s34 or "≠ Gate-5" in s34 or "not** Gate-5" in s34
    ops = OPS_README.read_text(encoding="utf-8")
    assert "STORY-AIBRIDGE-37" in ops
    assert "Gate-5" in ops
