# STORY-AIBRIDGE-57 — L11-1 invalidation seam

## Meta
- **Key:** `STORY-AIBRIDGE-57-l11-invalidation-seam`
- **Status:** Done · P8 · pkg-000060 · Product Done · 1524b49/13a992f/2f89ae4 · 2026-11-01T18:17:48Z · [pipeline](../../epics/EPIC-AIBRIDGE-09-req-11-req15-dual-confirm-gateway-submit-spa-handoff/stories/STORY-AIBRIDGE-57-l11-invalidation-seam/STORY-AIBRIDGE-57-l11-invalidation-seam.md) · [p3](../../run-reports/run-summary-20261101-1458-story-aibridge-57-p3.md) · [p4](../../analysis/p4-audit-STORY-AIBRIDGE-57-l11-invalidation-seam-20261101.md) · [p6](../../run-reports/run-summary-20261101-1813-story-aibridge-57-p6.md) · [p7](../../analysis/p7-reaudit-STORY-AIBRIDGE-57-l11-invalidation-seam-20261101.md)
- **Parent REQ:** [`REQ-11`](../../../requirements/REQ-11-REQ15-DUAL-CONFIRM-GATEWAY-SUBMIT-SPA-HANDOFF.md) §4.6 · AC-02 · L11-1
- **Tech-arch:** [`req15-dual-confirm-handoff/02-l11-invalidation-seam.md`](../../../architecture/req15-dual-confirm-handoff/02-l11-invalidation-seam.md)
- **Package:** [`INDEX.md`](INDEX.md)
- **Siblings:** [56](STORY-AIBRIDGE-56-keep-pipe-confirm-stash-spa-verify.md) · [58](STORY-AIBRIDGE-58-stub-live-evidence-gates.md)
- **Skill declared:** `python-pro` — [SKILL.md](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md)
- **Emitted:** 2026-11-01T14:15:37Z
- **Tech subtasks:** Present (arch-bound table below; pre-P1.3)
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../../.cursor/rules/analysis.mdc)

## Scope
- Named seam: semantic meaning-change (future) → **same invalidate effects** as EDIT (`apply_edit` → `invalidate_send_permission`: tokens, revision policy, clear gateway auth / continuation).
- Transition C: until REQ-13 semantic state Present, enforce remains Present EDIT/revision only; document + test EDIT path still Pass.
- Do **not** invent semantic field taxonomy or DB tables (REQ-13).

## Out of scope
- Implementing full semantic state store (REQ-13 stories).
- Sensitivity product list of fields.
- Keep-pipe re-verify (56) · evidence gates (58).
- Checker/PII role body (REQ-13 — operator Q1).

## Verified current state
- Named seam: `confirm.py:407–439` `invalidate_send_permission` (live).
- Transition C: `confirm.py:441–445` `apply_edit` → seam (live).
- Arch cites: `02`/`01`/`00` refreshed P6 t09 (no stale `407–425` as `apply_edit`).
- Semantic state store: **Absent** (T1 / REQ-13).
- Target A: **Partial** (documented in `runtime-docs/05-l11-invalidation-seam.md`).

## Target / AC
- [x] AC-AIB-11-02 (transition C): EDIT/revision invalidates dependent send permission — harness Pass.
- [x] Seam Present: single invalidate entry callable for future meaning-change **without** second permission store (unit/hook test; may be no-op caller until REQ-13).
- [ ] AC-AIB-11-02 target A: not claim Done until REQ-13 state Present + meaning-change evidence (document Partial vs Done gate) — **Partial**.

## Code points
- `src/aibridge/confirm.py` `invalidate_send_permission` · `apply_edit` · token `invalidate_session_revision`
- Hook name matches arch seam label `invalidate_send_permission()`; no new HTTP

## Technical subtasks (arch-bound; pre-P1.3)

| ID | Subtask | Arch cite | AC / DoD | Touch (as-is) | OOS | Status |
|----|---------|-----------|----------|---------------|-----|--------|
| **t01** | Spec seam effects = side-effects of `apply_edit` (tokens, revision, clear gateway auth / continuation) | [`02` §2](../../../architecture/req15-dual-confirm-handoff/02-l11-invalidation-seam.md) | AC-02 foundation | `confirm.py` seam + `apply_edit` | Field taxonomy | Done |
| **t02** | Named seam entry: used by EDIT + callable for future meaning-change; no second permission store; no HTTP/DB | [`02` §2–3](../../../architecture/req15-dual-confirm-handoff/02-l11-invalidation-seam.md) | Seam Present | `invalidate_send_permission` | Semantic state store (REQ-13) | Done |
| **t03** | Harness transition C: EDIT/revision remains sole enforce while state Absent | [`02` §3](../../../architecture/req15-dual-confirm-handoff/02-l11-invalidation-seam.md) | AC-AIB-11-02 transition C Pass | EDIT path harness | Target A Done claim | Done |
| **t04** | Unit: invoke seam without Telegram EDIT → same clearance as EDIT; keep target A **Partial** | [`02` §3](../../../architecture/req15-dual-confirm-handoff/02-l11-invalidation-seam.md) | Hook readiness for REQ-13 | Seam unit test | Meaning-change field invent | Done |
| **t05** | Doc note: AC-02 target A Done blocked until REQ-13 semantic state Present + evidence | [`02` §3–4](../../../architecture/req15-dual-confirm-handoff/02-l11-invalidation-seam.md) | Honesty Partial vs Done | `runtime-docs/05-…` | REQ-13 implement | Done |
| **t08** | Story gate checklist for 57 | [`00-overview`](../../../architecture/req15-dual-confirm-handoff/00-overview.md) L11-1 row | Package gate for 57 | After t01–t05 | 56/58 scopes | PASS |

## Dependencies
- STORY-AIBRIDGE-56
- Soft: REQ-13 for target A closure
