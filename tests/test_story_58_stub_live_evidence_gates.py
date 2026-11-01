"""STORY-AIBRIDGE-58 — AC-AIB-11-07 stub matrix + live Partial honesty (docs gate).

No invent live SUCCESS / Railway Pass. Runnable Keep-pipe harness remains story 56/57.
"""

from __future__ import annotations

from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
_DOC = _REPO / "docs" / "runtime-docs" / "06-ac07-stub-live-evidence-gates.md"
_INDEX = (
    _REPO
    / "docs"
    / "tasks"
    / "backlog-stories"
    / "req-11-req15-dual-confirm-gateway-submit-spa-handoff"
    / "INDEX.md"
)

# Wave honesty: live side Explicit Partial without ops window.
AC_AIB_11_07_LIVE_STATUS = "Partial"


def test_t01_stub_matrix_doc_maps_keep_pipe_harness() -> None:
    assert _DOC.is_file()
    text = _DOC.read_text(encoding="utf-8")
    assert "AC-AIB-11-01" in text
    assert "AC-AIB-11-03" in text
    assert "AC-AIB-11-04" in text
    assert "AC-AIB-11-05" in text
    assert "AC-AIB-11-06" in text
    assert "test_story_56_keep_pipe_confirm_stash_spa.py" in text
    assert (_REPO / "tests" / "test_story_56_keep_pipe_confirm_stash_spa.py").is_file()


def test_t02_live_runbook_explicit_partial_without_window() -> None:
    text = _DOC.read_text(encoding="utf-8")
    assert "Explicit Partial" in text
    assert "Unknown" in text
    assert AC_AIB_11_07_LIVE_STATUS == "Partial"
    # Must not claim live Done / invent Railway SUCCESS in this wave doc.
    assert "Railway live Pass" not in text
    assert "live SUCCESS" in text  # appears in Forbidden wording
    assert "Forbidden" in text or "Absent" in text


def test_t03_peer_verify_first_cites_present() -> None:
    text = _DOC.read_text(encoding="utf-8")
    assert "59-req15-story-draft-stash-channel-parity-verify.md" in text
    assert "25-req15-story-submit-handoff-continuity-verify.md" in text
    assert "REQ-01-REQ15-TELEGRAM-CHANNEL-TRANSPORT.md" in text
    root = _REPO.parent
    assert (
        root
        / "doge-complaints-gateway/docs/requirements/59-req15-story-draft-stash-channel-parity-verify.md"
    ).is_file()
    assert (
        root / "spa-app/docs/requirements/25-req15-story-submit-handoff-continuity-verify.md"
    ).is_file()
    assert (
        root / "doge-telegram/docs/requirements/REQ-01-REQ15-TELEGRAM-CHANNEL-TRANSPORT.md"
    ).is_file()


def test_t04_package_index_honesty_stub_ne_ac07_done() -> None:
    assert _INDEX.is_file()
    text = _INDEX.read_text(encoding="utf-8")
    assert "stub ≠ AC-AIB-11-07 Done" in text or "stub ≠ AC-AIB-11-07" in text
    assert "live only when ops window open" in text


def test_t08_runtime_readme_links_evidence_doc() -> None:
    readme = (_REPO / "docs" / "runtime-docs" / "README.md").read_text(encoding="utf-8")
    assert "06-ac07-stub-live-evidence-gates.md" in readme
