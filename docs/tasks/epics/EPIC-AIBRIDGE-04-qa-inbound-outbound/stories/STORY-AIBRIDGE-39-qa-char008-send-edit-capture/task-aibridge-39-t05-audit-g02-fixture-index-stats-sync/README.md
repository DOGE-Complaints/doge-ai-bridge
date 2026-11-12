# Task: test/docs — fixture-index stats + stories_covered sync (G-02)

**Status:** Done  
**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Wave:** `run_mode=aibridge_39_audit_20260918`  
**Gap:** G-02 (Medium) — P4 audit 2026-09-18  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-39-qa-char008-send-edit-capture-20260918.md`  
**Parent story:** [`STORY-AIBRIDGE-39-qa-char008-send-edit-capture.md`](../STORY-AIBRIDGE-39-qa-char008-send-edit-capture.md)  
**P5 scaffold:** 2026-09-18T14:14:24Z  
**P6 closed:** 2026-09-18T14:16:54Z  
**Maps:** CHAR-008 · fixture-index · gaps §39

## Purpose

Sync `fixture-index` integrity: `stats.fixture_count` = `len(fixtures)`; `stories_covered` includes STORY-39; bump `synced_at`. Assert in honesty suite. promote=copy package ↔ tests indexes. Docs/suite only.

**Out of this task:** invent n8n export / Send-Edit capture answers (G-01 WAIVED); QUAL prose (t06); live TG.

## AC/DoD

- [x] `stats.fixture_count` matches fixture rows; STORY-39 in `stories_covered`.
- [x] Honesty suite asserts stats/stories_covered.
- [x] Package ↔ tests fixture-index promote=copy / hash_eq as applicable.
- [x] No invent export / live TG.
- [x] `Skill declared: test-master` present.

## Where changed

- `tests/fixtures/meta/fixture-index.json` — stats 230 · stories_covered +39 · synced_at 14:16:54Z
- package `fixtures/fixture-index.json` — promote=copy hash_eq
- `tests/test_char008_send_edit_capture_honesty.py` — `test_char008_fixture_index_stats_stories_covered_sync`

## Evidence

```text
.venv/bin/python -m pytest tests/test_char008_send_edit_capture_honesty.py -q
5 passed
```
