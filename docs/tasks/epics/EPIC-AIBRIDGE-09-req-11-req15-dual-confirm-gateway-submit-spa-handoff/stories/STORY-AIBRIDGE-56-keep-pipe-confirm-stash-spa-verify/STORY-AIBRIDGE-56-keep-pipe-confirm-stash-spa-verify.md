# STORY-AIBRIDGE-56 — Keep pipe: dual-confirm + stash + SPA verify

## Meta
- **Key:** `STORY-AIBRIDGE-56-keep-pipe-confirm-stash-spa-verify`
- **Status:** P8 Done · Product Done · pkg-000059 · SHAs 8a4774e/db5f5ac/22bccc3 · 2026-11-01T14:51:13Z
- **P8 Commits:** 8a4774e feat · db5f5ac test · 22bccc3 docs · push=NO
- **P4 Audit:** 2026-11-01T14:42:50Z · [p4](../../../../analysis/p4-audit-STORY-AIBRIDGE-56-keep-pipe-confirm-stash-spa-verify-20261101.md)
- **P5 APPLY:** 2026-11-01T14:45:36Z · [p5 draft](../../../../../../.cursor/plans/p5_aibridge_56_gap_20261101T144423Z.plan.md) · G-01 WAIVED · G-02 TASKED→t09
- **P6 Execute:** 2026-11-01T14:47:16Z · t09 Done · [p6](../../../../run-reports/run-summary-20261101-1447-story-aibridge-56-p6.md)
- **P7 Re-audit:** 2026-11-01T14:49:58Z · [p7](../../../../analysis/p7-reaudit-STORY-AIBRIDGE-56-keep-pipe-confirm-stash-spa-verify-20261101.md)
- **Parent Epic:** [`EPIC-AIBRIDGE-09-req-11-req15-dual-confirm-gateway-submit-spa-handoff.md`](../../EPIC-AIBRIDGE-09-req-11-req15-dual-confirm-gateway-submit-spa-handoff.md)
- **source:** `backlog-stories/req-11-req15-dual-confirm-gateway-submit-spa-handoff/STORY-AIBRIDGE-56-keep-pipe-confirm-stash-spa-verify.md`
- **decision_ref:** [`STORY-AIBRIDGE-56-….md`](../../../../backlog-stories/req-11-req15-dual-confirm-gateway-submit-spa-handoff/STORY-AIBRIDGE-56-keep-pipe-confirm-stash-spa-verify.md) · [`REQ-11`](../../../../requirements/REQ-11-REQ15-DUAL-CONFIRM-GATEWAY-SUBMIT-SPA-HANDOFF.md) · [`01-keep-pipe-boundaries.md`](../../../../architecture/req15-dual-confirm-handoff/01-keep-pipe-boundaries.md)
- **Package:** [`req-11-req15-dual-confirm-gateway-submit-spa-handoff/INDEX.md`](../../../../backlog-stories/req-11-req15-dual-confirm-gateway-submit-spa-handoff/INDEX.md)
- **Skill declared:** `python-pro`
- **Active pkg (wave):** `pkg-000059-20261101-epic-aibridge-09-story-56-keep-pipe-confirm-stash-spa-verify.yaml`
- **P1 materialize:** 2026-11-01T14:34:14Z · [p1 APPLIED](../../../../../../.cursor/plans/p1_aibridge_56_scaffold_20261101T143252Z.plan.md)
- **P3 Execute:** 2026-11-01T14:40:28Z · [p3](../../../../run-reports/run-summary-20261101-1438-story-aibridge-56-p3.md) · tests **587 passed**
- **Gate:** [t08](./task-aibridge-56-t08-story-gate-checklist/README.md) · **PASS**
- **Depends:** soft tech-arch Present · none on 57/58

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| Keep pipe boundaries | [`01-keep-pipe-boundaries.md`](../../../../architecture/req15-dual-confirm-handoff/01-keep-pipe-boundaries.md) |
| Confirm/gateway Keep SSOT | [`runtime/03-confirm-gateway.md`](../../../../architecture/runtime/03-confirm-gateway.md) |
| Runtime note | [`04-confirm-gateway-keep-pipe.md`](../../../../runtime-docs/04-confirm-gateway-keep-pipe.md) |
| Arch overview | [`00-overview.md`](../../../../architecture/req15-dual-confirm-handoff/00-overview.md) |

## Scope
- Re-verify Present server pipe: interpretation confirm ≠ send confirm; ActionToken + revision/`draft_hash` (arch D3 reuse).
- Gateway submit URL + Bearer only from bridge config (`GatewayExecutor`); model cannot supply arbitrary URL.
- User-visible success only after factual stash success; continuation `{SPA}/#/story/submit?draft_id=`.
- Prove telegram/channel path does not perform stash (secrets on bridge).
- Harness/tests + thin runtime note if missing — **Keep**, not rewrite FSM/gateway API.

## Вне scope
- L11-1 semantic seam implement (57); stub/live evidence gates doc (58).
- Gateway schema / SPA UX redesign (peers 59/25).
- REQ-12 providers · GPT-48 instruction rewrite · NEW confirm store.
- Checker/PII role body (REQ-13 — operator Q1).

## Target / AC
- [x] AC-AIB-11-01: two distinct confirm stages enforced in harness.
- [x] AC-AIB-11-03: submit URL from config only.
- [x] AC-AIB-11-04: success only after factual gateway success.
- [x] AC-AIB-11-05: continuation uses Present SPA hash + `draft_id`.
- [x] AC-AIB-11-06: no stash from telegram-service responsibility (bridge-owned client).

**Implement (P3):** `tests/test_story_56_keep_pipe_confirm_stash_spa.py` · `docs/runtime-docs/04-confirm-gateway-keep-pipe.md` · Keep Present confirm/gateway (no FSM/API rewrite).

## Nested tasks (pkg-000059)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-56-t01-dual-confirm-stages-harness](./task-aibridge-56-t01-dual-confirm-stages-harness/README.md) | AC-AIB-11-01 | Done |
| t02 | [task-aibridge-56-t02-confirm-storage-actiontoken-reuse](./task-aibridge-56-t02-confirm-storage-actiontoken-reuse/README.md) | AC-01 support | Done |
| t03 | [task-aibridge-56-t03-tool-intent-freeze-not-gateway-permission](./task-aibridge-56-t03-tool-intent-freeze-not-gateway-permission/README.md) | Keep · D4 | Done |
| t04 | [task-aibridge-56-t04-gateway-executor-config-url-bearer](./task-aibridge-56-t04-gateway-executor-config-url-bearer/README.md) | AC-AIB-11-03 | Done |
| t05 | [task-aibridge-56-t05-factual-stash-success-outcomes](./task-aibridge-56-t05-factual-stash-success-outcomes/README.md) | AC-AIB-11-04 | Done |
| t06 | [task-aibridge-56-t06-continuation-spa-hash-draft-id](./task-aibridge-56-t06-continuation-spa-hash-draft-id/README.md) | AC-AIB-11-05 | Done |
| t07 | [task-aibridge-56-t07-bridge-owns-stash-channel-boundary](./task-aibridge-56-t07-bridge-owns-stash-channel-boundary/README.md) | AC-AIB-11-06 | Done |
| t08 | [task-aibridge-56-t08-story-gate-checklist](./task-aibridge-56-t08-story-gate-checklist/README.md) | gate | PASS |
| t09 | [task-aibridge-56-t09-audit-g02-backlog-tech-table-sync](./task-aibridge-56-t09-audit-g02-backlog-tech-table-sync/README.md) | P4 G-02 | Done |
