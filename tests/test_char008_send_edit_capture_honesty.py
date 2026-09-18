"""STORY-AIBRIDGE-39 — CHAR-008 Send/Edit capture honesty (no invent export / live TG).

Export absent → capture envelope status=deferred with visible defer_reason.
When export lands later: response_states + retry_dedupe_policy must be non-empty.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

from fixture_loader import FIXTURES_ROOT, load_fixture

BRIDGE_ROOT = Path(__file__).resolve().parent.parent
PKG_CAP = (
    BRIDGE_ROOT
    / "docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/fixtures/n8n/char-008-send-edit-capture.json"
)
EXPORT = (
    BRIDGE_ROOT
    / "docs/ops/n8n-channel-workflow/exports/aibridge-telegram-channel-v1.json"
)
OBS = (
    BRIDGE_ROOT
    / "docs/tasks/epics/EPIC-AIBRIDGE-04-qa-inbound-outbound/stories"
    / "STORY-AIBRIDGE-39-qa-char008-send-edit-capture"
    / "task-aibridge-39-t01-observe-workflow-outbound"
    / "observation-note-20260918-1406.md"
)


def test_char008_capture_promoted_hash_eq() -> None:
    assert PKG_CAP.is_file()
    promoted = FIXTURES_ROOT / "n8n" / "char-008-send-edit-capture.json"
    assert promoted.is_file()
    assert hashlib.sha256(PKG_CAP.read_bytes()).hexdigest() == hashlib.sha256(
        promoted.read_bytes()
    ).hexdigest()


def test_char008_capture_deferred_or_filled() -> None:
    """Behavioral assert beyond file-presence: defer visible XOR capture non-empty."""
    env = load_fixture("n8n", "char-008-send-edit-capture")
    assert env["schema_version"] == "1.0"
    assert env["fixture_id"] == "n8n.char-008-send-edit-capture"
    assert "CHAR-008" in env["matrix_ids"]
    payload = env["payload"]
    status = payload["status"]
    assert status in ("deferred", "captured")
    if status == "deferred":
        defer = payload.get("defer_reason") or ""
        assert defer.strip(), "deferred capture must expose defer_reason"
        assert payload.get("response_states") == []
        assert payload.get("retry_dedupe_policy") is None
        assert payload.get("source_export_sha256") is None
        assert not EXPORT.is_file(), "export present but capture still deferred — re-capture"
        assert "invent" in defer.lower() or "absent" in defer.lower()
    else:
        states = payload.get("response_states") or []
        assert states, "captured CHAR-008 requires non-empty response_states"
        for row in states:
            assert row.get("telegram_api") in ("send_message", "edit_message")
        assert (payload.get("retry_dedupe_policy") or "").strip()
        assert (payload.get("source_export_sha256") or "").strip()


def test_char008_observation_and_pin_pointer_linked() -> None:
    assert OBS.is_file()
    text = OBS.read_text(encoding="utf-8")
    assert "ABSENT" in text or "absent" in text.lower()
    pin = load_fixture("meta", "n8n-wf-001-pin-pointer")
    assert pin["payload"]["status"] == "deferred"
    env = load_fixture("n8n", "char-008-send-edit-capture")
    assert env["payload"].get("pin_pointer_ref") == "meta/n8n-wf-001-pin-pointer.json"
    ops = env["payload"].get("ops_readme_notes") or {}
    assert ops.get("source") == "ops_readme_not_export"


PKG_INDEX = (
    BRIDGE_ROOT
    / "docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/fixtures/fixture-index.json"
)
STORY_39 = "STORY-AIBRIDGE-39-qa-char008-send-edit-capture"


def test_char008_fixture_index_row_and_program_defer() -> None:
    idx = load_fixture("meta", "fixture-index")
    assert STORY_39 in idx["story_keys"]
    rows = {f["fixture_id"]: f for f in idx["payload"]["fixtures"]}
    assert "n8n.char-008-send-edit-capture" in rows
    chars = {c["id"]: c for c in idx["payload"]["program"]["characterization"]}
    row = chars["CHAR-008"]
    assert row.get("defer_reason")
    assert "n8n/char-008-send-edit-capture.json" in (row.get("refs") or [])
    assert any(
        "test_char008_send_edit_capture_honesty" in b for b in (row.get("bound_tests") or [])
    )


def test_char008_fixture_index_stats_stories_covered_sync() -> None:
    """G-02: stats.fixture_count == len(fixtures); stories_covered includes STORY-39; promote hash_eq."""
    assert PKG_INDEX.is_file()
    promoted = FIXTURES_ROOT / "meta" / "fixture-index.json"
    assert promoted.is_file()
    assert hashlib.sha256(PKG_INDEX.read_bytes()).hexdigest() == hashlib.sha256(
        promoted.read_bytes()
    ).hexdigest()
    idx = load_fixture("meta", "fixture-index")
    stats = idx["payload"]["stats"]
    fixtures = idx["payload"]["fixtures"]
    assert stats["fixture_count"] == len(fixtures)
    assert STORY_39 in stats["stories_covered"]
    assert (stats.get("synced_at") or "").strip()
