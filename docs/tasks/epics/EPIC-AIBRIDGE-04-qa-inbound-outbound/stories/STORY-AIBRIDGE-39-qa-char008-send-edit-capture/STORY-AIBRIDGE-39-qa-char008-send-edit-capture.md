# STORY-AIBRIDGE-39 — QA — CHAR-008 Send/Edit + dedupe capture

## Meta
- **Key:** `STORY-AIBRIDGE-39-qa-char008-send-edit-capture`
- **Status:** ✅ Done (P3) · P6 gap close · next P7 · `run_mode=aibridge_39_audit_20260918` · 2026-09-18T14:16:54Z — CHAR-008 **deferred** (export absent)
- **Parent Epic:** [`EPIC-AIBRIDGE-04-qa-inbound-outbound.md`](../../EPIC-AIBRIDGE-04-qa-inbound-outbound.md)
- **source:** `backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-39-qa-char008-send-edit-capture.md`
- **decision_ref:** [`STORY-AIBRIDGE-39-….md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-39-qa-char008-send-edit-capture.md) · [`TECHNICAL-ARCHITECTURE-GAPS-36-40.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/TECHNICAL-ARCHITECTURE-GAPS-36-40.md) §39 · guide §16 CHAR-008
- **Parent SSOT:** [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md)
- **Package:** [`qa-inbound-outbound-data-flow/INDEX.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/INDEX.md)
- **Qualification:** closes **P1-Q3** (closed-with-defer)
- **Skill declared:** `python-pro` · `test-master`
- **Active pkg (wave):** `pkg-000038-20260918-epic-aibridge-04-story-39-qa-char008-send-edit-capture.yaml` (immutable under `run_mode=aibridge_39_audit_20260918`)
- **P1 materialize:** 2026-09-18T14:03:38Z
- **P3 closed:** 2026-09-18T14:06:43Z · capture deferred · honesty 4 + gates DoD
- **P5 APPLY:** 2026-09-18T14:14:24Z · t05–t06 scaffold
- **P6 closed:** 2026-09-18T14:16:54Z · G-02/G-03 CLOSED · honesty 5
- **Gate:** [t04](./task-aibridge-39-t04-story-gate/README.md) PASS · t05–t06 Done

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| Gaps §39 CHAR-008 | [`TECHNICAL-ARCHITECTURE-GAPS-36-40.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/TECHNICAL-ARCHITECTURE-GAPS-36-40.md) §39 |
| Ops README §2 Send/Edit | [`docs/ops/n8n-channel-workflow/README.md`](../../../../ops/n8n-channel-workflow/README.md) |
| N8N-WF-001 pin pointer | `tests/fixtures/meta/n8n-wf-001-pin-pointer.json` (deferred · export absent) |
| Capture envelope | package `fixtures/n8n/char-008-send-edit-capture.json` · promote copy `tests/fixtures/n8n/` |
| Honesty suite | `tests/test_char008_send_edit_capture_honesty.py` |

## Scope
Capture-first statements for **CHAR-008**: Send Message vs Edit Message per response state + n8n retry dedupe — real capture, not file-presence alone.

## Вне scope
- Invent export body / Send/Edit policy without evidence; Gate-5 (STORY-37); invent live TG; delete/move package fixtures originals.

## Context
P1-Q3: file-presence ≠ answered Send vs Edit. Export pin **absent** → visible defer + behavioral honesty path (P3).

## Use cases / matrix IDs

| ID | Scenario | Expected |
|----|----------|----------|
| CHAR-008 | Send vs Edit + retry dedupe | Captured answer **or** explicit visible `defer_reason` |

## Target / AC
- [x] CHAR-008 owned by this story key.
- [x] Capture answers Send vs Edit + retry dedupe — **or** defer_reason remains **visible** (export absent · deferred envelope).
- [x] Meta path checks OK; behavioral assert required for Done.
- [x] Nested tasks Done (2026-09-18T14:06:43Z).
- [x] P1-Q3 closed-with-defer.

## Nested tasks (pkg-000038 + audit override)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-39-t01-observe-workflow-outbound](./task-aibridge-39-t01-observe-workflow-outbound/README.md) | export+README observe / defer | Done |
| t02 | [task-aibridge-39-t02-capture-fixture](./task-aibridge-39-t02-capture-fixture/README.md) | char-008 envelope · promote=copy | Done |
| t03 | [task-aibridge-39-t03-bind-behavioral-assert](./task-aibridge-39-t03-bind-behavioral-assert/README.md) | non-empty capture or visible defer | Done |
| t04 | [task-aibridge-39-t04-story-gate](./task-aibridge-39-t04-story-gate/README.md) | TRACEABILITY + P1-Q3 | Done |
| t05 | [task-aibridge-39-t05-audit-g02-fixture-index-stats-sync](./task-aibridge-39-t05-audit-g02-fixture-index-stats-sync/README.md) | G-02 fixture-index stats | Done |
| t06 | [task-aibridge-39-t06-audit-g03-qual-map-closed-with-defer](./task-aibridge-39-t06-audit-g03-qual-map-closed-with-defer/README.md) | G-03 QUAL map | Done |
