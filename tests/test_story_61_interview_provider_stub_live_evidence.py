"""STORY-AIBRIDGE-61 — AC-AIB-12-04 stub matrix + live Partial honesty (docs gate).

No invent live SUCCESS / Railway Pass. Runnable harness remains story 59/60.
"""

from __future__ import annotations

from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
_DOC = _REPO / "docs" / "runtime-docs" / "08-ac04-interview-stub-live-evidence-gates.md"
_INDEX = (
    _REPO
    / "docs"
    / "tasks"
    / "backlog-stories"
    / "req-12-req15-interview-deepseek-openai-providers"
    / "INDEX.md"
)

# Wave honesty: live side Explicit Partial without ops window (both providers).
AC_AIB_12_04_LIVE_STATUS = "Partial"


def test_t01_stub_matrix_doc_maps_59_60_harness() -> None:
    assert _DOC.is_file()
    text = _DOC.read_text(encoding="utf-8")
    assert "AC-AIB-12-01" in text
    assert "AC-AIB-12-02" in text
    assert "AC-AIB-12-03" in text
    assert "AC-AIB-12-05" in text
    assert "test_story_59_interview_port_env_fail_closed.py" in text
    assert "test_story_60_openai_deepseek_interview_adapters.py" in text
    assert (_REPO / "tests" / "test_story_59_interview_port_env_fail_closed.py").is_file()
    assert (
        _REPO / "tests" / "test_story_60_openai_deepseek_interview_adapters.py"
    ).is_file()


def test_t02_live_runbook_explicit_partial_without_window() -> None:
    text = _DOC.read_text(encoding="utf-8")
    assert "Explicit Partial" in text
    assert "Unknown" in text
    assert "deepseek" in text
    assert "openai" in text
    assert AC_AIB_12_04_LIVE_STATUS == "Partial"
    assert "Railway" in text and ("Forbidden" in text or "Absent" in text)
    assert "live SUCCESS" in text
    # Must not claim live Done for either provider in this wave doc.
    assert "live Pass claimed" not in text.lower()


def test_t03_peer_cite_table_present() -> None:
    text = _DOC.read_text(encoding="utf-8")
    assert "ai-provider-selection/00-overview.md" in text
    assert "req15-dual-confirm-handoff/00-overview.md" in text
    assert "REQ-13-REQ15-SEMANTIC-STATE-ROLES-INSTRUCTION-ASSEMBLY.md" in text
    assert "REQ-48" in text
    assert "no model keys" in text.lower() or "No model keys" in text
    assert (
        _REPO / "docs" / "architecture" / "ai-provider-selection" / "00-overview.md"
    ).is_file()
    assert (
        _REPO / "docs" / "architecture" / "req15-dual-confirm-handoff" / "00-overview.md"
    ).is_file()


def test_t04_package_index_honesty_stub_ne_ac04_done() -> None:
    assert _INDEX.is_file()
    text = _INDEX.read_text(encoding="utf-8")
    assert "stub ≠ AC-AIB-12-04" in text
    assert "ops window" in text
    assert "no invent" in text.lower() or "no invent" in text


def test_t08_runtime_readme_links_evidence_doc() -> None:
    readme = (_REPO / "docs" / "runtime-docs" / "README.md").read_text(encoding="utf-8")
    assert "08-ac04-interview-stub-live-evidence-gates.md" in readme
