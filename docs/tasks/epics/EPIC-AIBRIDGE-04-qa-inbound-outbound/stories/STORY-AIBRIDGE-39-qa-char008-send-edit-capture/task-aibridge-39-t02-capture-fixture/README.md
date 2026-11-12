# Task: fixture — CHAR-008 Send/Edit capture envelope (promote=copy)

**Status:** Done · 2026-09-18T14:06:43Z  
**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-39-qa-char008-send-edit-capture.md`  
**Parent story:** [`STORY-AIBRIDGE-39-qa-char008-send-edit-capture.md`](../STORY-AIBRIDGE-39-qa-char008-send-edit-capture.md)  
**P1 scaffold:** 2026-09-18T14:03:38Z  
**Maps:** CHAR-008 · gaps §39 T02 · promote=copy

## Purpose

Write package `fixtures/n8n/char-008-send-edit-capture.json` per gaps §39 schema (`response_states`, `retry_dedupe_policy`, `source_export_path`, `source_export_sha256`); promote=**copy** to `tests/fixtures/n8n/`. If export still absent — keep defer envelope / visible `defer_reason` without inventing capture answers.

**Out of this task:** observe (t01); behavioral bind (t03); invent export body.

## AC/DoD

- [x] Capture fixture created **or** defer remains visible (name ≠ invent answers).
- [x] Promote = copy only (do not move/delete package originals).
- [x] No invent Send/Edit policy without evidence.
- [x] `Skill declared: test-master` present.

## Where to change (execute — not P1)

- `docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/fixtures/n8n/char-008-send-edit-capture.json` — **P3**
- `tests/fixtures/n8n/char-008-send-edit-capture.json` (copy) — **P3**
