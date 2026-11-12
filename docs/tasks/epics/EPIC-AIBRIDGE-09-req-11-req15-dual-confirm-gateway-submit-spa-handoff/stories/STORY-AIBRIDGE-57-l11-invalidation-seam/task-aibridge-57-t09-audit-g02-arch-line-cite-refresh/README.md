# Task: audit G-02 — arch line-cite refresh

**Status:** Done · P6 2026-11-01T18:13:35Z  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-11-req15-dual-confirm-gateway-submit-spa-handoff/STORY-AIBRIDGE-57-l11-invalidation-seam.md`  
**Parent story:** [`STORY-AIBRIDGE-57-l11-invalidation-seam.md`](../STORY-AIBRIDGE-57-l11-invalidation-seam.md)  
**P5 scaffold:** 2026-11-01T18:11:35Z · [p5 DRAFT](../../../../../../../../.cursor/plans/p5_aibridge_57_gap_20261101T150221Z.plan.md) · APPLIED into `aibridge_builder.plan.md`  
**P6 close:** 2026-11-01T18:13:35Z · `run_mode=aibridge_57_audit_20261101`  
**Maps:** P4 G-02 · Info · `run_mode=aibridge_57_audit_20261101`

## Purpose

Refresh stale `confirm.py` line cites in arch `02-l11-invalidation-seam.md` §2 (and peer arch cites of the same span if present): `407–425` no longer labels `apply_edit`; seam is `invalidate_send_permission` (~407–439), `apply_edit` (~441–445). Doc-only hygiene — no product code · no REQ-13 invent.

## AC/DoD

- [x] Arch `docs/architecture/req15-dual-confirm-handoff/02-l11-invalidation-seam.md` line cites match Present `confirm.py` seam/`apply_edit`.
- [x] Peer arch files in same package that still cite `407–425` as `apply_edit` refreshed or noted Absent.
- [x] No invent REQ-13 taxonomy / DB / second permission store / new HTTP.
- [x] Target A remains **Partial** (G-01 WAIVED).
- [x] `Skill declared: python-pro` present.
- [x] No product invent beyond this task DoD.

## Where changed (P6)

- `docs/architecture/req15-dual-confirm-handoff/02-l11-invalidation-seam.md` — §2 cite → `441–445` `apply_edit` → `407–439` seam
- `docs/architecture/req15-dual-confirm-handoff/01-keep-pipe-boundaries.md` — EDIT path cite refreshed
- `docs/architecture/req15-dual-confirm-handoff/00-overview.md` — L11-1 row cite refreshed

## Evidence

- Acceptance: [`acceptance-verification-task-aibridge-57-t09-audit-g02-arch-line-cite-refresh.md`](./acceptance-verification-task-aibridge-57-t09-audit-g02-arch-line-cite-refresh.md)
- Code facts: `confirm.py:407` `invalidate_send_permission` · `confirm.py:441` `apply_edit`
